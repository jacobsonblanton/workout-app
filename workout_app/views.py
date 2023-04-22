# importing the necessary modules 
from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint, json, Markup
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_manager, login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Coach, Client, Weight
from sqlalchemy import delete, update, text
from datetime import date, timedelta
from sqlalchemy.sql import func

views = Blueprint('views', __name__)

# getting everyday of the current year
# this method will allow us to compare the datetime of database entry to the current date
def everyday_of_current_year(year):
    d = date(year, 1, 1) # getting the first monday
    d += timedelta(days = 7 - d.weekday()) # adding every day to d
    while d.year == year: # looping through the entire year while the d.year is equal to the specified year. 
        yield d
        d += timedelta(days = 1) # since we will prompt the user evryday, we add 1 to the current day
        
table = []
for d in everyday_of_current_year(2023):
    table.append(d.strftime("%m-%d"))
#print(table)

# removing the zeros and empty strings from the list of weights that is pulled from the weight table 
def removing_zeroes(x):
    
    for i in x:
        if i == '':
            x.remove(i)
            return removing_zeroes(x)
        elif i <= 0:
            x.remove(i)
            return removing_zeroes(x)
        
    return x

# removing the same dates from the label list, so the graph will only show that day once
# this wont be necessary after the database is deleted and re-created. Fixed this issue with 
# the update clause in the home() method.
def removing_same_days(x):
    for i in range(0,len(x)):
        for j in range(i+1, len(x)):
            if x[i] == x[j]:
                x.remove(x[i])
                return removing_same_days(x)
    return x

# accessing the home page 
@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    # establishing the necessary variables for plotting the weight data in the line graph
    data = Weight.query.with_entities(Weight.new_weight, Weight.date_created).all()
    #dates = db.session.query(Weight).get(Weight.date_created)
    #print(dates)
    labels = [row[1] for row in data]
    formatted_labels = []
    for label in labels:
        formatted_label = label.strftime("%Y-%m-%d")
        formatted_labels.append(formatted_label)
    
    values = [row[0] for row in data]
    removing_zeroes(x=values)
    removing_same_days(x=formatted_labels)

    labels = formatted_labels
    #weights = Weight.query(Weight.new_weight).all()
    # updating the Weight table if the date created is the same
    now = datetime.now()
    today = now.date()
    today = str(today)
    #sql = text("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='upper_2day'")
    weight_date = text("SELECT count(date_created) FROM WEIGHT WHERE date_created='2023-01-07'")
    result = db.session.execute(weight_date).fetchall()
    #print(result)
    date_created = Weight.query.with_entities(Weight.date_created).all()
    created_dates = [row[0] for row in date_created]
    formatted_date_created = []
    for date in created_dates:
        dates = date.strftime("%Y-%m-%d")
        formatted_date_created.append(dates)
    #print(dates)
    print(formatted_date_created)
    if len(formatted_date_created) >= 2:
        if formatted_date_created[len(formatted_date_created)-1] == formatted_date_created[len(formatted_date_created)-2]:
            # if the user already has a weight entered for the current day,
            # that weight is deleted and replaced with the newly entered weight
            update_weight = delete(Weight).where(Weight.date_created == today)
            db.session.execute(update_weight)
            db.session.commit()
    coach = Coach.query.first()
    print(coach.user.first_name)
    

    if request.method == 'POST':
        weights = Weight.query.filter(Weight.new_weight)
        new_weight = request.form.get("newWeight-content")
        if new_weight == '':
            flash('Weight cannot be empty!', category='error')
         
        else:
            new_weight = Weight(user_id=current_user.id, new_weight=new_weight)
            db.session.add(new_weight)
            db.session.commit()
        # deleting the weights that are less than 10 kg (not realistic to be under 10 kg)
        # deleting the weights that are empty ''
        delete_weight = delete(Weight).where(Weight.new_weight < 10)
        db.session.execute(delete_weight)
        db.session.commit()
        # deleting the weights that are empty ''
        delete_empty_weight = delete(Weight).where(Weight.new_weight == '')
        db.session.execute(delete_empty_weight)
        db.session.commit()
        
        return render_template("home.html", user=current_user, first_name=current_user.first_name, weight=weights, 
        values=values, labels=labels)

    else:
        return render_template("home.html", user=current_user, first_name=current_user.first_name, 
        values=values, labels=labels)

# accessing the user's profile page 
@views.route('/profile/<first_name>', methods=['POST', 'GET'])
@login_required
def profile_page(first_name):
    if request.method == 'POST':
        pass
    else:
        first_name = db.session.query(User).get(current_user.first_name)
        user_info = db.session.query(User).all()
        return render_template("profile.html", user=current_user, first_name=first_name, user_info=user_info) 

# accessing the calorie calculator page
@views.route('/calorie-calculator', methods=['POST', 'GET'])
@login_required
def calorie_calculator():
    if request.method == 'POST':
        weight = current_user.starting_weight
        height = current_user.height
        age = current_user.age
        gender = current_user.gender
        # getting bmr equation based on user input and printing the bmr
        male_bmr = round(88.362 + (13.397 * weight) + (4.799 * height ) - (5.677 * age),2)
        female_bmr = round(447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age),2)

        # determining which equation to use based on gender of the user
        if gender == 'male' or 'Male':
            print("Your basal metabolic rate is", male_bmr, "kcal.")
        elif gender == 'female' or 'Female':
            print("Your basal metabolic rate is", female_bmr, "kcal.")
        else:
            print("gender must be male or female...")

        # asking the user a few more questions to determine how many calories to add to their bmr
        job = db.session.query(User).get(current_user.job_type)
        job_type = request.form.get('jobType-content')
        # adding the job type to the database
        print(job_type)
        job = job_type
        current_user.job_type = job
        db.session.commit()
        flash('Job type added!', category='success')

        cardio = request.form.get('cardio-content')
        weight_training = request.form.get('weightTraining-content')

        # implementing a while loop for male and female so I can add calories to correct bmr value
        while gender == 'male' or gender == 'Male':
            if job_type == 'sedentary':
                male_bmr += 300
                print("...calculating your new bmr")
                print("Your new bmr is", round(male_bmr,2), "kcal.")
                
            elif job_type == 'sedentary-active':
                male_bmr += 500
                print("...calculating your new bmr")
                print("Your new bmr is", round(male_bmr,2), "kcal.")

            elif job_type == 'active-sedentary':
                male_bmr += 700
                print("...calculating your new bmr")
                print("Your new bmr is", round(male_bmr,2), "kcal.")

            elif job_type == 'active':
                male_bmr += 900
                print("...calculating your new bmr")
                print("Your new bmr is", round(male_bmr,2), "kcal.")

            elif job_type == '' or cardio == '' or weight_training == '':
                flash('No field can be left empty!', category='error')
                return redirect(url_for('views.calorie_calculator'))

            else:
                print("Enter a valid selection.")

            # updating user calories into the database
            cals = db.session.query(User).get(current_user.cals)
            cals = male_bmr
            current_user.cals = cals
            db.session.commit()
            print(cals)
            print(round(cals*7.00,2))
            flash('BMR added!', category='success')
            return redirect(url_for('views.calorie_calculator_result'))


        while gender == 'female' or gender == 'Female':
            if job_type == 'sedentary':
                female_bmr += 300
                print("...calculating your new bmr")
                
                print("Your new bmr is", round(female_bmr,2), "kcal.")
            elif job_type == 'sedentary-active':
                female_bmr += 500
                print("...calculating your new bmr")
                print("Your new bmr is", round(female_bmr,2), "kcal.")
            
            elif job_type == 'active-sedentary':
                female_bmr += 700
                print("...calculating your new bmr")
                print("Your new bmr is", round(female_bmr,2), "kcal.")
            
            elif job_type == 'active':
                female_bmr += 900
                print("...calculating your new bmr")
                print("Your new bmr is", round(female_bmr,2), "kcal.")

            else:
                print("Enter a valid selection.")
            
            cals = db.session.query(User).get(current_user.cals)
            cals = female_bmr
            current_user.cals = cals
            db.session.commit()
            print(cals)
            flash('BMR added!', category='success')
            return redirect(url_for('views.calorie_calculator_result'))
                            
        return render_template("calorie_calculator_result.html", user=current_user)

    else:

        return render_template("calorie_calculator.html", user=current_user)

# setting the calorie result page
@views.route('/calorie-calculator-result', methods=['POST', 'GET'])
@login_required
def calorie_calculator_result():
    if request.method == 'GET':
        if current_user.gender == 'male' or 'Male':

            
            return render_template("calorie_calculator_result.html", user=current_user, gender=current_user.gender, cals=current_user.cals)
        elif current_user.gender == 'female' or 'Female':
            
            return render_template("calorie_calculator_result.html", user=current_user, gender=current_user.gender, cals=current_user.cals) 
        

# accessing the workout automation page
import random 
@views.route('/workout-automation', methods=['POST', 'GET'])
@login_required
def workout_automation():
    if request.method == 'POST':
        # getting the inputs from the user from the workout automation page
        workout_days = request.form.get('workout-days-content')
        db.session.query(User).get(current_user.workout_days)
        current_user.workout_days = workout_days
        db.session.commit()
        training_focus = request.form.get('training-focus-content')
        db.session.query(User).get(current_user.training_focus)
        current_user.training_focus = training_focus
        db.session.commit()
        session_time = request.form.get('session-time-content')

        # creating a list of exercises for each workout day 
        # seperated by type of exercise and what muscle group is being worked 
        hor_push_exercises = ['smith machine bench', 'db bench', 'db incline bench', 'pushups', 'smith machine incline bench']
        chest_iso_exercises = ['cable flys', 'db flys', 'pec deck']
        vert_push_exercises = ['overhead shoulder press', 'arnold press', 'dips', 'db shoulder press']
        hor_pull_exercises = ['smith machine bent rows', 'cable rows', 'chest supported row', 'smith machine underhand bent rows']
        vert_pull_exercises = ['wide-grip-pullups', 'wide-grip-pull downs', 'close-grip pulldown', 'close-grip-pullups']
        back_iso_exercises = ['lat prayers', 'rear delt flys', 'single-arm rows']
        quad_exercises = ['smith machine squat', 'leg press', 'bulgarian split squat', 'smith machine split squat']
        quad_iso_exercises = ['leg extension']
        ham_exercises = ['smith machine rdl', 'db rdl', 'single leg squat', 'lunges']
        ham_iso_exercises = ['leg curl']
        calf_exercises = ['smith machine calf raises', 'seated calf raises', 'leg press calf raises']
        bi_exercises = ['db curl', 'db hammer curl', 'rope curl', 'preacher curls']
        tri_exercises = ['overhead tri extension', 'tri rope push downs', 'skull crushers', 'close grip bench']
        shoulder_exercises = ['db lateral raises', 'cable lateral raises', 'cable Y raises', 'cable upright rows', 'barbell upright rows']

        # creating a function to define the automation of each workout split,
        # dependent on the questions answered on the workout automation page
        if workout_days == '6':
            if training_focus == 'hypertrophy':
                def upper_lower_six():
                    # Upper Day 1
                    upper_one = []
                    up = hor_push_exercises 
                    up2 = vert_push_exercises
                    up3 = hor_pull_exercises
                    up4 = vert_pull_exercises
                    up5 = bi_exercises

                    upper_one.append(random.choice(up))
                    upper_one.append(random.choice(up2))
                    upper_one.append(random.choice(up3))
                    upper_one.append(random.choice(up4))
                    upper_one.append(random.choice(up5))

                    # if there is already a row with id = 1, then the row is deleted and new columns are added
                    # otherwise the row is created 
                    upper_table_results = db.session.query(Upper_One).filter(Upper_One.id)

                    if upper_table_results != 1:

                        delete_row = delete(Upper_One).where(Upper_One.id==1)
                        db.session.execute(delete_row)
                        exercise1 = upper_one[0]
                        exercise2 = upper_one[1]
                        exercise3 = upper_one[2]
                        exercise4 = upper_one[3]
                        exercise5 = upper_one[4]
                        exercises = Upper_One(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5)
                        db.session.add(exercises)
                        db.session.commit()
                        print(exercises)
                    
                    else:

                        exercise1 = upper_one[0]
                        exercise2 = upper_one[1]
                        exercise3 = upper_one[2]
                        exercise4 = upper_one[3]
                        exercise5 = upper_one[4]
                        exercises = Upper_One(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5)
                        db.session.add(exercises)
                        db.session.commit()

                    # Lower Day 1
                    lower_one = []
                    low1 = quad_exercises
                    low2 = ham_exercises
                    low3 = calf_exercises
                    shoulder1 = shoulder_exercises

                    lower_one.append(random.choice(low1))
                    lower_one.append(random.choice(low2))
                    lower_one.append(random.choice(low3))
                    lower_one.append(random.choice(shoulder1))

                    lower_table_results = db.session.query(Lower_One).filter(Lower_One.id)

                    if lower_table_results != 1:

                        delete_row = delete(Lower_One).where(Lower_One.id==1)
                        db.session.execute(delete_row)
                        exercise1 = lower_one[0]
                        exercise2 = lower_one[1]
                        exercise3 = lower_one[2]
                        exercise4 = lower_one[3]
                        exercises = Lower_One(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4)
                        db.session.add(exercises)
                        db.session.commit()

                    else:

                        exercise1 = lower_one[0]
                        exercise2 = lower_one[1]
                        exercise3 = lower_one[2]
                        exercise4 = lower_one[3]
                        exercises = Lower_One(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4)
                        db.session.add(exercises)
                        db.session.commit()

                    # create new function here 
                    def upper_day_two():
                        # Upper Day 2
                        upper_two = []
                        up6 = tri_exercises
                        upper_two.append(random.choice(up))
                        upper_two.append(random.choice(up2))
                        upper_two.append(random.choice(up3))
                        upper_two.append(random.choice(up4))
                        upper_two.append(random.choice(up6))
                        # checking if the exercise exists in the previous upper day 
                        # if the exercise exists, remove the exercise from current list and re-run the loop
                        for elem in upper_two:
                            if elem in upper_one:
                                upper_two.remove(elem)
                                return upper_day_two()

                        upper_table_results = db.session.query(Upper_Two).filter(Upper_Two.id)

                        if upper_table_results != 1:

                            delete_row = delete(Upper_Two).where(Upper_Two.id==1)
                            db.session.execute(delete_row)
                            exercise1 = upper_two[0]
                            exercise2 = upper_two[1]
                            exercise3 = upper_two[2]
                            exercise4 = upper_two[3]
                            exercise5 = upper_two[4]
                            exercises = Upper_Two(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5)
                            db.session.add(exercises)
                            db.session.commit()

                        else:

                            exercise1 = upper_two[0]
                            exercise2 = upper_two[1]
                            exercise3 = upper_two[2]
                            exercise4 = upper_two[3]
                            exercise5 = upper_two[4]
                            exercises = Upper_Two(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5)
                            db.session.add(exercises)
                            db.session.commit()

                        return upper_two
                    # create new function here 
                    def lower_day_two():
                        # Lower Day 2 
                        lower_two = []
                        low1 = quad_exercises
                        low2 = ham_exercises
                        low3 = calf_exercises
                        shoulder1 = shoulder_exercises

                        lower_two.append(random.choice(low1))
                        lower_two.append(random.choice(low2))
                        lower_two.append(random.choice(low3))
                        lower_two.append(random.choice(shoulder1))
                        # checking if the exercise exists in the previous lower day 
                        # if the exercise exists, remove the exercise from current list and re-run the loop
                        for elem in lower_two:
                            if elem in lower_one:
                                lower_two.remove(elem)
                                return lower_day_two()

                        lower_table_results = db.session.query(Lower_Two).filter(Lower_Two.id)

                        if lower_table_results != 1:

                            delete_row = delete(Lower_Two).where(Lower_Two.id==1)
                            db.session.execute(delete_row)
                            exercise1 = lower_two[0]
                            exercise2 = lower_two[1]
                            exercise3 = lower_two[2]
                            exercise4 = lower_two[3]
                            exercises = Lower_Two(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4)
                            db.session.add(exercises)
                            db.session.commit()

                        else:
                            exercise1 = lower_two[0]
                            exercise2 = lower_two[1]
                            exercise3 = lower_two[2]
                            exercise4 = lower_two[3]
                            exercises = Lower_Two(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4)
                            db.session.add(exercises)
                            db.session.commit()

                        return lower_two
                    # create new function here 
                    def upper_day_three():
                        # Upper Day 3 
                        upper_three = []
                        upper_three.append(random.choice(up))
                        upper_three.append(random.choice(up2))
                        upper_three.append(random.choice(up3))
                        upper_three.append(random.choice(up4))
                        upper_three.append(random.choice(up5))
                        # checking if the exercise exists in the 2 previous upper days 
                        # if the exercise exists, remove the exercise from current list and re-run the loop
                        for elem in upper_three:
                            if elem in upper_one and elem in upper_day_two():
                                upper_three.remove(elem)
                                return upper_day_three()

                        upper_table_results = db.session.query(Upper_Three).filter(Upper_Three.id)

                        if upper_table_results != 1:

                            delete_row = delete(Upper_Three).where(Upper_Three.id==1)
                            db.session.execute(delete_row)
                            exercise1 = upper_three[0]
                            exercise2 = upper_three[1]
                            exercise3 = upper_three[2]
                            exercise4 = upper_three[3]
                            exercise5 = upper_three[4]
                            exercises = Upper_Three(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5)
                            db.session.add(exercises)
                            db.session.commit()

                        else:

                            exercise1 = upper_three[0]
                            exercise2 = upper_three[1]
                            exercise3 = upper_three[2]
                            exercise4 = upper_three[3]
                            exercise5 = upper_three[4]
                            exercises = Upper_Three(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5)
                            db.session.add(exercises)
                            db.session.commit()

                        return upper_three
                    # create new function here 
                    def lower_day_three():
                        # Lower Day 3 
                        lower_three = []
                        low1 = quad_exercises
                        low2 = ham_exercises
                        low3 = calf_exercises
                        shoulder1 = shoulder_exercises

                        lower_three.append(random.choice(low1))
                        lower_three.append(random.choice(low2))
                        lower_three.append(random.choice(low3))
                        lower_three.append(random.choice(shoulder1))
                        # checking if the exercise exists in the previous lower day 
                        # if the exercise exists, remove the exercise from current list and re-run the loop
                        for elem in lower_three:
                            if elem in lower_one and elem in lower_day_two():
                                lower_three.remove(elem)
                                return lower_day_three()

                        lower_table_results = db.session.query(Lower_Three).filter(Lower_Three.id)

                        if lower_table_results != 1:

                            delete_row = delete(Lower_Three).where(Lower_Three.id==1)
                            db.session.execute(delete_row)
                            exercise1 = lower_three[0]
                            exercise2 = lower_three[1]
                            exercise3 = lower_three[2]
                            exercise4 = lower_three[3]
                            exercises = Lower_Three(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4)
                            db.session.add(exercises)
                            db.session.commit()

                        else:

                            exercise1 = lower_three[0]
                            exercise2 = lower_three[1]
                            exercise3 = lower_three[2]
                            exercise4 = lower_three[3]
                            exercises = Lower_Three(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4)
                            db.session.add(exercises)
                            db.session.commit()

                        return lower_three
                        

                    #print('Upper/Lower 6 Day Routine')
                    #print('Upper 1',upper_one)
                    #print('Lower 1',lower_one)
                    upper_day_two()
                    lower_day_two()
                    upper_day_two()
                    lower_day_three()
                    upper_day_three()
                    #return redirect(url_for('views.workout_automation_result'))


                return redirect(url_for("views.workout_automation_result", user=current_user, upper_lower=upper_lower_six(), workout_days=workout_days, training_focus=training_focus)) 
            
            else:
                pass
        elif workout_days == '5':
            if training_focus == 'hypertrophy':
                def UL_PPL():
                    
                    #lower day 1
                    def UL_PPL_day_one():
                        ul_ppl_one = []
                        ul_ppl_one.append(random.choice(quad_exercises))
                        ul_ppl_one.append(random.choice(quad_exercises))
                        if ul_ppl_one[0] == ul_ppl_one[1]:
                            for elem in ul_ppl_one:
                                ul_ppl_one.remove(elem)
                                return UL_PPL_day_one()
                        ul_ppl_one.append(random.choice(ham_exercises))
                        ul_ppl_one.append(random.choice(quad_iso_exercises))
                        ul_ppl_one.append(random.choice(bi_exercises))
                        ul_ppl_one.append(random.choice(shoulder_exercises))
                     
                        ul_ppl_one_table_res = db.session.query(UL_PPL_One).filter(UL_PPL_One.id)

                        if ul_ppl_one_table_res != 1:

                            delete_row = delete(UL_PPL_One).where(UL_PPL_One.id==1)
                            db.session.execute(delete_row)
                            exercise1 = ul_ppl_one[0]
                            exercise2 = ul_ppl_one[1]
                            exercise3 = ul_ppl_one[2]
                            exercise4 = ul_ppl_one[3]
                            exercise5 = ul_ppl_one[4]
                            exercise6 = ul_ppl_one[5]
                            exercsies = UL_PPL_One(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = ul_ppl_one[0]
                            exercise2 = ul_ppl_one[1]
                            exercise3 = ul_ppl_one[2]
                            exercise4 = ul_ppl_one[3]
                            exercise5 = ul_ppl_one[4]
                            exercise6 = ul_ppl_one[5]
                            exercsies = UL_PPL_One(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6)
                            db.session.add(exercsies)
                            db.session.commit()


                        return ul_ppl_one
                    # upper day 2
                    def UL_PPL_day_two():
                        ul_ppl_two = []
                        ul_ppl_two.append(random.choice(hor_pull_exercises))
                        ul_ppl_two.append(random.choice(hor_push_exercises))
                        ul_ppl_two.append(random.choice(vert_pull_exercises))
                        ul_ppl_two.append(random.choice(vert_push_exercises))
                        ul_ppl_two.append(random.choice(chest_iso_exercises))
                        ul_ppl_two.append(random.choice(back_iso_exercises))
                        ul_ppl_two.append(random.choice(calf_exercises))



                        ul_ppl_two_table_res = db.session.query(UL_PPL_Two).filter(UL_PPL_Two.id)

                        if ul_ppl_two_table_res != 1:

                            delete_row = delete(UL_PPL_Two).where(UL_PPL_Two.id==1)
                            db.session.execute(delete_row)
                            exercise1 = ul_ppl_two[0]
                            exercise2 = ul_ppl_two[1]
                            exercise3 = ul_ppl_two[2]
                            exercise4 = ul_ppl_two[3]
                            exercise5 = ul_ppl_two[4]
                            exercise6 = ul_ppl_two[5]
                            exercise7 = ul_ppl_two[6]
                            exercsies = UL_PPL_Two(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = ul_ppl_two[0]
                            exercise2 = ul_ppl_two[1]
                            exercise3 = ul_ppl_two[2]
                            exercise4 = ul_ppl_two[3]
                            exercise5 = ul_ppl_two[4]
                            exercise6 = ul_ppl_two[5]
                            exercise7 = ul_ppl_two[6]
                            exercsies = UL_PPL_Two(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7)
                            db.session.add(exercsies)
                            db.session.commit()

                        return ul_ppl_two
                    # legs day 3
                    def UL_PPL_day_three():
                        ul_ppl_three = []
                        ul_ppl_three.append(random.choice(ham_exercises))
                        ul_ppl_three.append(random.choice(ham_exercises))
                        # removing the duplicate exercises from the list
                        if ul_ppl_three[0] == ul_ppl_three[1]:
                            for elem in ul_ppl_three:
                                ul_ppl_three.remove(elem)
                                return UL_PPL_day_three()
                        ul_ppl_three.append(random.choice(quad_exercises))
                        ul_ppl_three.append(random.choice(ham_iso_exercises))
                        ul_ppl_three.append(random.choice(tri_exercises))
                        ul_ppl_three.append(random.choice(shoulder_exercises))
                        
                        for elem in ul_ppl_three:
                            if elem in UL_PPL_day_one() and elem in UL_PPL_day_two():
                                ul_ppl_three.remove(elem)
                                return UL_PPL_day_three()

                        ul_ppl_three_table_res = db.session.query(UL_PPL_Three).filter(UL_PPL_Three.id)

                        if ul_ppl_three_table_res != 1:

                            delete_row = delete(UL_PPL_Three).where(UL_PPL_Three.id==1)
                            db.session.execute(delete_row)
                            exercise1 = ul_ppl_three[0]
                            exercise2 = ul_ppl_three[1]
                            exercise3 = ul_ppl_three[2]
                            exercise4 = ul_ppl_three[3]
                            exercise5 = ul_ppl_three[4]
                            exercise6 = ul_ppl_three[5]
                            exercsies = UL_PPL_Three(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = ul_ppl_three[0]
                            exercise2 = ul_ppl_three[1]
                            exercise3 = ul_ppl_three[2]
                            exercise4 = ul_ppl_three[3]
                            exercise5 = ul_ppl_three[4]
                            exercise6 = ul_ppl_three[5]
                            exercsies = UL_PPL_Three(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6)
                            db.session.add(exercsies)
                            db.session.commit()

                        return ul_ppl_three

                    # push day 4
                    def UL_PPL_day_four():
                        ul_ppl_four = []
                        ul_ppl_four.append(random.choice(vert_push_exercises))
                        ul_ppl_four.append(random.choice(hor_push_exercises))
                        ul_ppl_four.append(random.choice(vert_push_exercises))
                        ul_ppl_four.append(random.choice(hor_push_exercises))
                        if ul_ppl_four[0] == ul_ppl_four[2]:
                            for elem in ul_ppl_four:
                                ul_ppl_four.remove(elem)
                            return UL_PPL_day_four()
                        elif ul_ppl_four[1] == ul_ppl_four[3]:
                            for elem in ul_ppl_four:
                                ul_ppl_four.remove(elem)
                            return UL_PPL_day_four()

                        ul_ppl_four.append(random.choice(bi_exercises))
                        ul_ppl_four.append(random.choice(calf_exercises))
                        ul_ppl_four.append(random.choice(chest_iso_exercises))

                        for elem in ul_ppl_four:
                            if elem in UL_PPL_day_one() and elem in UL_PPL_day_two():
                                    ul_ppl_four.remove(elem)
                                    return UL_PPL_day_four()

                        ul_ppl_four_table_res = db.session.query(UL_PPL_Four).filter(UL_PPL_Four.id)

                        if ul_ppl_four_table_res != 1:

                            delete_row = delete(UL_PPL_Four).where(UL_PPL_Four.id==1)
                            db.session.execute(delete_row)
                            exercise1 = ul_ppl_four[0]
                            exercise2 = ul_ppl_four[1]
                            exercise3 = ul_ppl_four[2]
                            exercise4 = ul_ppl_four[3]
                            exercise5 = ul_ppl_four[4]
                            exercise6 = ul_ppl_four[5]
                            exercise7 = ul_ppl_four[6]
                            exercsies = UL_PPL_Four(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = ul_ppl_four[0]
                            exercise2 = ul_ppl_four[1]
                            exercise3 = ul_ppl_four[2]
                            exercise4 = ul_ppl_four[3]
                            exercise5 = ul_ppl_four[4]
                            exercise6 = ul_ppl_four[5]
                            exercise7 = ul_ppl_four[6]
                            exercsies = UL_PPL_Four(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7)
                            db.session.add(exercsies)
                            db.session.commit()

                        return ul_ppl_four

                    # pull day 5
                    def UL_PPL_day_five():
                        ul_ppl_five = []
                        ul_ppl_five.append(random.choice(vert_pull_exercises))
                        ul_ppl_five.append(random.choice(hor_pull_exercises))
                        ul_ppl_five.append(random.choice(vert_pull_exercises))
                        ul_ppl_five.append(random.choice(hor_pull_exercises))
                        if ul_ppl_five[0] == ul_ppl_five[2]:
                            for elem in ul_ppl_five:
                                ul_ppl_five.remove(elem)
                            return UL_PPL_day_five()
                        elif ul_ppl_five[1] == ul_ppl_five[3]:
                            for elem in ul_ppl_five:
                                ul_ppl_five.remove(elem)
                            return UL_PPL_day_five()
                        ul_ppl_five.append(random.choice(tri_exercises))

                        for elem in ul_ppl_five:
                            if elem in UL_PPL_day_two() and elem in UL_PPL_day_three():
                                ul_ppl_five.remove(elem)
                                return UL_PPL_day_five()

                        ul_ppl_five_table_res = db.session.query(UL_PPL_Five).filter(UL_PPL_Five.id)

                        if ul_ppl_five_table_res != 1:

                            delete_row = delete(UL_PPL_Five).where(UL_PPL_Five.id==1)
                            db.session.execute(delete_row)
                            exercise1 = ul_ppl_five[0]
                            exercise2 = ul_ppl_five[1]
                            exercise3 = ul_ppl_five[2]
                            exercise4 = ul_ppl_five[3]
                            exercise5 = ul_ppl_five[4]
                            exercsies = UL_PPL_Five(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = ul_ppl_five[0]
                            exercise2 = ul_ppl_five[1]
                            exercise3 = ul_ppl_five[2]
                            exercise4 = ul_ppl_five[3]
                            exercise5 = ul_ppl_five[4]
                            exercsies = UL_PPL_Five(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5)
                            db.session.add(exercsies)
                            db.session.commit()

                        return ul_ppl_five

                    print('\nUpper, Lower, Push, Pull, Legs 5 Day Routine')
                    print('Day 1',UL_PPL_day_one())
                    print('Day 2',UL_PPL_day_two())
                    print('Day 3',UL_PPL_day_three())
                    print('Day 4',UL_PPL_day_four())
                    print('Day 5',UL_PPL_day_five())


                return redirect(url_for('views.workout_automation_result', user=current_user, ul_ppl=UL_PPL()))
            else:
                pass
        elif workout_days == '4':
            if training_focus == 'hypertrophy':
                def full_body_4():
                    #full body day 1
                    def full_body_day_one():
                        full_body_one = []
                        full_body_one.append(random.choice(hor_push_exercises))
                        full_body_one.append(random.choice(quad_exercises))
                        full_body_one.append(random.choice(quad_exercises))
                        full_body_one.append(random.choice(chest_iso_exercises))
                        full_body_one.append(random.choice(vert_push_exercises))
                        full_body_one.append(random.choice(tri_exercises))
                        full_body_one.append(random.choice(calf_exercises))
                        full_body_one.append(random.choice(shoulder_exercises))

                        full_body_one_table_res = db.session.query(Full_Body_One_4day).filter(Full_Body_One_4day.id)

                        if full_body_one_table_res != 1:

                            delete_row = delete(Full_Body_One_4day).where(Full_Body_One_4day.id==1)
                            db.session.execute(delete_row)
                            exercise1 = full_body_one[0]
                            exercise2 = full_body_one[1]
                            exercise3 = full_body_one[2]
                            exercise4 = full_body_one[3]
                            exercise5 = full_body_one[4]
                            exercise6 = full_body_one[5]
                            exercise7 = full_body_one[6]
                            exercise8 = full_body_one[7]
                            exercsies = Full_Body_One_4day(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7, exercise8=exercise8)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = full_body_one[0]
                            exercise2 = full_body_one[1]
                            exercise3 = full_body_one[2]
                            exercise4 = full_body_one[3]
                            exercise5 = full_body_one[4]
                            exercise6 = full_body_one[5]
                            exercise7 = full_body_one[6]
                            exercise8 = full_body_one[7]
                            exercsies = Full_Body_One_4day(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7, exercise8=exercise8)
                            db.session.add(exercsies)
                            db.session.commit()


                        return full_body_one
                    # full body day 2
                    def full_body_day_two():
                        full_body_two = []
                        full_body_two.append(random.choice(hor_pull_exercises))
                        full_body_two.append(random.choice(vert_pull_exercises))
                        full_body_two.append(random.choice(bi_exercises))
                        full_body_two.append(random.choice(ham_exercises))
                        full_body_two.append(random.choice(bi_exercises))
                        full_body_two.append(random.choice(shoulder_exercises))
                    
                        for elem in full_body_two:
                            if elem in full_body_day_one():
                                full_body_two.remove(elem)
                                return full_body_day_two()

                        full_body_two_table_res = db.session.query(Full_Body_Two_4day).filter(Full_Body_Two_4day.id)

                        if full_body_two_table_res != 1:

                            delete_row = delete(Full_Body_Two_4day).where(Full_Body_Two_4day.id==1)
                            db.session.execute(delete_row)
                            exercise1 = full_body_two[0]
                            exercise2 = full_body_two[1]
                            exercise3 = full_body_two[2]
                            exercise4 = full_body_two[3]
                            exercise5 = full_body_two[4]
                            exercise6 = full_body_two[5]
                            exercsies = Full_Body_Two_4day(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = full_body_two[0]
                            exercise2 = full_body_two[1]
                            exercise3 = full_body_two[2]
                            exercise4 = full_body_two[3]
                            exercise5 = full_body_two[4]
                            exercise6 = full_body_two[5]
                            exercsies = Full_Body_Two_4day(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6)
                            db.session.add(exercsies)
                            db.session.commit()

                        return full_body_two
                    # full body day 3
                    def full_body_day_three():
                        full_body_three = []
                        full_body_three.append(random.choice(vert_push_exercises))
                        full_body_three.append(random.choice(hor_pull_exercises))
                        full_body_three.append(random.choice(quad_exercises))
                        full_body_three.append(random.choice(quad_iso_exercises))
                        full_body_three.append(random.choice(tri_exercises))
                        full_body_three.append(random.choice(calf_exercises))
                        full_body_three.append(random.choice(shoulder_exercises))

                        for elem in full_body_three:
                            if elem in full_body_day_one() and elem in full_body_day_two():
                                full_body_three.remove(elem)
                                return full_body_day_three()

                        full_body_three_table_res = db.session.query(Full_Body_Three_4day).filter(Full_Body_Three_4day.id)

                        if full_body_three_table_res != 1:

                            delete_row = delete(Full_Body_Three_4day).where(Full_Body_Three_4day.id==1)
                            db.session.execute(delete_row)
                            exercise1 = full_body_three[0]
                            exercise2 = full_body_three[1]
                            exercise3 = full_body_three[2]
                            exercise4 = full_body_three[3]
                            exercise5 = full_body_three[4]
                            exercise6 = full_body_three[5]
                            exercise7 = full_body_three[6]
                            exercsies = Full_Body_Three_4day(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = full_body_three[0]
                            exercise2 = full_body_three[1]
                            exercise3 = full_body_three[2]
                            exercise4 = full_body_three[3]
                            exercise5 = full_body_three[4]
                            exercise6 = full_body_three[5]
                            exercise7 = full_body_three[6]
                            exercsies = Full_Body_Three_4day(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7)
                            db.session.add(exercsies)
                            db.session.commit()

                        return full_body_three

                    # full body day 4
                    def full_body_day_four():
                        full_body_four = []
                        full_body_four.append(random.choice(vert_pull_exercises))
                        full_body_four.append(random.choice(hor_pull_exercises))
                        full_body_four.append(random.choice(ham_exercises))
                        full_body_four.append(random.choice(ham_iso_exercises))
                        full_body_four.append(random.choice(bi_exercises))
                        full_body_four.append(random.choice(bi_exercises))
                        full_body_four.append(random.choice(shoulder_exercises))

                        for elem in full_body_four:
                            if elem in full_body_day_one() and elem in full_body_day_two() and elem in full_body_day_three():
                                full_body_four.remove(elem)
                                return full_body_day_four()

                        full_body_four_table_res = db.session.query(Full_Body_Four_4day).filter(Full_Body_Four_4day.id)

                        if full_body_four_table_res != 1:

                            delete_row = delete(Full_Body_Four_4day).where(Full_Body_Four_4day.id==1)
                            db.session.execute(delete_row)
                            exercise1 = full_body_four[0]
                            exercise2 = full_body_four[1]
                            exercise3 = full_body_four[2]
                            exercise4 = full_body_four[3]
                            exercise5 = full_body_four[4]
                            exercise6 = full_body_four[5]
                            exercise7 = full_body_four[6]
                            exercsies = Full_Body_Four_4day(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = full_body_four[0]
                            exercise2 = full_body_four[1]
                            exercise3 = full_body_four[2]
                            exercise4 = full_body_four[3]
                            exercise5 = full_body_four[4]
                            exercise6 = full_body_four[5]
                            exercise7 = full_body_four[6]
                            exercsies = Full_Body_Four_4day(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7)
                            db.session.add(exercsies)
                            db.session.commit()

                        return full_body_four

                    print('\nFull Body 4 Day Routine')
                    print('Day 1',full_body_day_one())
                    print('Day 2',full_body_day_two())
                    print('Day 3',full_body_day_three())
                    print('Day 4',full_body_day_four())


                return redirect(url_for('views.workout_automation_result', user=current_user, full_body=full_body_4()))
            else:
                pass
        elif workout_days == '3':
            if training_focus == 'hypertrophy':
                def full_body_3():
                    #full body day 1
                    def full_body_day_one():
                        full_body_one = []
                        full_body_one.append(random.choice(hor_push_exercises))
                        full_body_one.append(random.choice(hor_pull_exercises))
                        full_body_one.append(random.choice(quad_exercises))
                        full_body_one.append(random.choice(ham_exercises))
                        full_body_one.append(random.choice(bi_exercises))
                        full_body_one.append(random.choice(tri_exercises))
                        full_body_one.append(random.choice(calf_exercises))
                        full_body_one.append(random.choice(shoulder_exercises))

                        full_body_one_table_res = db.session.query(Full_Body_One).filter(Full_Body_One.id)

                        if full_body_one_table_res != 1:

                            delete_row = delete(Full_Body_One).where(Full_Body_One.id==1)
                            db.session.execute(delete_row)
                            exercise1 = full_body_one[0]
                            exercise2 = full_body_one[1]
                            exercise3 = full_body_one[2]
                            exercise4 = full_body_one[3]
                            exercise5 = full_body_one[4]
                            exercise6 = full_body_one[5]
                            exercise7 = full_body_one[6]
                            exercise8 = full_body_one[7]
                            exercsies = Full_Body_One(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7, exercise8=exercise8)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = full_body_one[0]
                            exercise2 = full_body_one[1]
                            exercise3 = full_body_one[2]
                            exercise4 = full_body_one[3]
                            exercise5 = full_body_one[4]
                            exercise6 = full_body_one[5]
                            exercise7 = full_body_one[6]
                            exercise8 = full_body_one[7]
                            exercsies = Full_Body_One(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7, exercise8=exercise8)
                            db.session.add(exercsies)
                            db.session.commit()


                        return full_body_one
                    # full body day 2
                    def full_body_day_two():
                        full_body_two = []
                        full_body_two.append(random.choice(chest_iso_exercises))
                        full_body_two.append(random.choice(back_iso_exercises))
                        full_body_two.append(random.choice(quad_iso_exercises))
                        full_body_two.append(random.choice(ham_iso_exercises))
                        full_body_two.append(random.choice(bi_exercises))
                        full_body_two.append(random.choice(tri_exercises))
                        full_body_two.append(random.choice(calf_exercises))
                        full_body_two.append(random.choice(shoulder_exercises))
                    
                        for elem in full_body_two:
                            if elem in full_body_day_one():
                                full_body_two.remove(elem)
                                return full_body_day_two()

                        full_body_two_table_res = db.session.query(Full_Body_Two).filter(Full_Body_Two.id)

                        if full_body_two_table_res != 1:

                            delete_row = delete(Full_Body_Two).where(Full_Body_Two.id==1)
                            db.session.execute(delete_row)
                            exercise1 = full_body_two[0]
                            exercise2 = full_body_two[1]
                            exercise3 = full_body_two[2]
                            exercise4 = full_body_two[3]
                            exercise5 = full_body_two[4]
                            exercise6 = full_body_two[5]
                            exercise7 = full_body_two[6]
                            exercise8 = full_body_two[7]
                            exercsies = Full_Body_Two(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7, exercise8=exercise8)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = full_body_two[0]
                            exercise2 = full_body_two[1]
                            exercise3 = full_body_two[2]
                            exercise4 = full_body_two[3]
                            exercise5 = full_body_two[4]
                            exercise6 = full_body_two[5]
                            exercise7 = full_body_two[6]
                            exercise8 = full_body_two[7]
                            exercsies = Full_Body_Two(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7, exercise8=exercise8)
                            db.session.add(exercsies)
                            db.session.commit()

                        return full_body_two
                    # full body day 3
                    def full_body_day_three():
                        full_body_three = []
                        full_body_three.append(random.choice(vert_push_exercises))
                        full_body_three.append(random.choice(vert_pull_exercises))
                        full_body_three.append(random.choice(quad_exercises))
                        full_body_three.append(random.choice(ham_exercises))
                        full_body_three.append(random.choice(bi_exercises))
                        full_body_three.append(random.choice(tri_exercises))
                        full_body_three.append(random.choice(calf_exercises))
                        full_body_three.append(random.choice(shoulder_exercises))

                        for elem in full_body_three:
                            if elem in full_body_day_one() and elem in full_body_day_two():
                                full_body_three.remove(elem)
                                return full_body_day_three()

                        full_body_three_table_res = db.session.query(Full_Body_Three).filter(Full_Body_Three.id)

                        if full_body_three_table_res != 1:

                            delete_row = delete(Full_Body_Three).where(Full_Body_Three.id==1)
                            db.session.execute(delete_row)
                            exercise1 = full_body_three[0]
                            exercise2 = full_body_three[1]
                            exercise3 = full_body_three[2]
                            exercise4 = full_body_three[3]
                            exercise5 = full_body_three[4]
                            exercise6 = full_body_three[5]
                            exercise7 = full_body_three[6]
                            exercise8 = full_body_three[7]
                            exercsies = Full_Body_Three(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7, exercise8=exercise8)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = full_body_three[0]
                            exercise2 = full_body_three[1]
                            exercise3 = full_body_three[2]
                            exercise4 = full_body_three[3]
                            exercise5 = full_body_three[4]
                            exercise6 = full_body_three[5]
                            exercise7 = full_body_three[6]
                            exercise8 = full_body_three[7]
                            exercsies = Full_Body_Three(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7, exercise8=exercise8)
                            db.session.add(exercsies)
                            db.session.commit()


                        return full_body_three
                    print('\nFull Body 3 Day Routine')
                    print('Day 1',full_body_day_one())
                    print('Day 2',full_body_day_two())
                    print('Day 3',full_body_day_three())

                return redirect(url_for('views.workout_automation_result', user=current_user, full_body=full_body_3()))
            else:
                pass
        elif workout_days == '2':
            if training_focus == 'hypertrophy':
                def UL_2day():
                    #full body day 1
                    def upper():
                        upper = []
                        upper.append(random.choice(hor_push_exercises))
                        upper.append(random.choice(hor_pull_exercises))
                        upper.append(random.choice(vert_push_exercises))
                        upper.append(random.choice(vert_push_exercises))
                        upper.append(random.choice(bi_exercises))
                        upper.append(random.choice(tri_exercises))
                        upper.append(random.choice(chest_iso_exercises))
                        upper.append(random.choice(back_iso_exercises))

                        upper_table_res = db.session.query(Upper_2day).filter(Upper_2day.id)

                        if upper_table_res != 1:

                            delete_row = delete(Upper_2day).where(Upper_2day.id==1)
                            db.session.execute(delete_row)
                            exercise1 = upper[0]
                            exercise2 = upper[1]
                            exercise3 = upper[2]
                            exercise4 = upper[3]
                            exercise5 = upper[4]
                            exercise6 = upper[5]
                            exercise7 = upper[6]
                            exercise8 = upper[7]
                            exercsies = Upper_2day(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7, exercise8=exercise8)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = upper[0]
                            exercise2 = upper[1]
                            exercise3 = upper[2]
                            exercise4 = upper[3]
                            exercise5 = upper[4]
                            exercise6 = upper[5]
                            exercise7 = upper[6]
                            exercise8 = upper[7]
                            exercsies = Upper_2day(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6, exercise7=exercise7, exercise8=exercise8)
                            db.session.add(exercsies)
                            db.session.commit()


                        return upper
                    # full body day 2
                    def lower():
                        lower = []
                        lower.append(random.choice(quad_exercises))
                        lower.append(random.choice(quad_iso_exercises))
                        lower.append(random.choice(ham_exercises))
                        lower.append(random.choice(ham_iso_exercises))
                        lower.append(random.choice(calf_exercises))
                        lower.append(random.choice(shoulder_exercises))
                    

                        lower_table_res = db.session.query(Lower_2day).filter(Lower_2day.id)

                        if lower_table_res != 1:

                            delete_row = delete(Lower_2day).where(Lower_2day.id==1)
                            db.session.execute(delete_row)
                            exercise1 = lower[0]
                            exercise2 = lower[1]
                            exercise3 = lower[2]
                            exercise4 = lower[3]
                            exercise5 = lower[4]
                            exercise6 = lower[5]
                            exercsies = Lower_2day(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6)
                            db.session.add(exercsies)
                            db.session.commit()

                        else:

                            exercise1 = lower[0]
                            exercise2 = lower[1]
                            exercise3 = lower[2]
                            exercise4 = lower[3]
                            exercise5 = lower[4]
                            exercise6 = lower[5]
                            exercsies = Lower_2day(user_id=current_user.id, exercise1=exercise1, exercise2=exercise2, exercise3=exercise3, exercise4=exercise4, exercise5=exercise5, 
                                                        exercise6=exercise6)
                            db.session.add(exercsies)
                            db.session.commit()

                        return lower
                    print('Day 1',upper())
                    print('Day 2',lower())
                return redirect(url_for('views.workout_automation_result', user=current_user, UL_2day=UL_2day()))
            else:
                pass
        return render_template("workout_automation_result.html", user=current_user)

    else: 
        return render_template("workout_automation.html", user=current_user)

@views.route('/workout-automation-result', methods=['POST', 'GET'])
@login_required
def workout_automation_result():
    if request.method == 'GET':
        # getting the Upper/Lower 6 Day exercises from the table database
        upper_1 = db.session.query(Upper_One).get(1)
        lower_1 = db.session.query(Lower_One).get(1)
        upper_2 = db.session.query(Upper_Two).get(1)
        lower_2 = db.session.query(Lower_Two).get(1)
        upper_3 = db.session.query(Upper_Three).get(1)
        lower_3 = db.session.query(Lower_Three).get(1)
        
        # getting the full body 3 Day exercises from the table in the database 
        full_body_1 = db.session.query(Full_Body_One).get(1)
        full_body_2 = db.session.query(Full_Body_Two).get(1)
        full_body_3 = db.session.query(Full_Body_Three).get(1)

        # getting the full body 4 Day exercises from the table in the database
        full_body4_1 = db.session.query(Full_Body_One_4day).get(1)
        full_body4_2 = db.session.query(Full_Body_Two_4day).get(1)
        full_body4_3 = db.session.query(Full_Body_Three_4day).get(1)
        full_body4_4 = db.session.query(Full_Body_Four_4day).get(1)

        # getting the uppper/lower-full body 5 day exercises from the table in the database
        ul_ppl_1 = db.session.query(UL_PPL_One).get(1)
        ul_ppl_2 = db.session.query(UL_PPL_Two).get(1)
        ul_ppl_3 = db.session.query(UL_PPL_Three).get(1)
        ul_ppl_4 = db.session.query(UL_PPL_Four).get(1)
        ul_ppl_5 = db.session.query(UL_PPL_Five).get(1)

        # getting the full body 2 day exercises from the table in the database
        ul_upper = db.session.query(Upper_2day).get(1)
        ul_lower = db.session.query(Lower_2day).get(1)
        # add each exercise that is committed to each model class
        # this will allow for accessing each exercise from each possible workkout split defined in the workout automation method  
        return render_template("workout_automation_result.html", user=current_user, upper_one=upper_1, lower_one=lower_1,
                                upper_two=upper_2, lower_two=lower_2, upper_three=upper_3, lower_three=lower_3, full_body_one=full_body_1,
                                full_body_two=full_body_2, full_body_three=full_body_3, full_body4_one=full_body4_1, full_body4_two=full_body4_2,
                                full_body4_three=full_body4_3, full_body4_four=full_body4_4, ul_ppl_one=ul_ppl_1,ul_ppl_two=ul_ppl_2, ul_ppl_three=ul_ppl_3,
                                ul_ppl_four=ul_ppl_4, ul_ppl_five=ul_ppl_5, ul_upper=ul_upper, ul_lower=ul_lower) 
# displaying all the workouts the user has currently generated
@views.route('/workouts', methods=['POST', 'GET'])
@login_required
def workouts():
    if request.method == 'GET':
        # getting the Upper/Lower 6 Day exercises from the table database

        # checking the table exists in the database
        #sql = text("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='upper_2day'")

        # getting the columns in the table for the workout and storing the result in a variable that can be rendered via jinja2 templating. 
        # only have to check the columns from one table in this workout because if one is empty then so are the rest.
        exercises = text("SELECT exercise1, exercise2, exercise3, exercise4, exercise5 FROM Upper__One ")
        upper_one_result = db.session.execute(exercises).fetchall()
        
        upper_1 = db.session.query(Upper_One).get(1)
        lower_1 = db.session.query(Lower_One).get(1)
        upper_2 = db.session.query(Upper_Two).get(1)
        lower_2 = db.session.query(Lower_Two).get(1)
        upper_3 = db.session.query(Upper_Three).get(1)
        lower_3 = db.session.query(Lower_Three).get(1)
        
        # getting the full body 3 Day exercises from the table in the database 
        full_body_3_exercises = text("SELECT exercise1, exercise2, exercise3, exercise4, exercise5 FROM Full__Body__One ")
        full_body_3_result = db.session.execute(full_body_3_exercises).fetchall()

        full_body_1 = db.session.query(Full_Body_One).get(1)
        full_body_2 = db.session.query(Full_Body_Two).get(1)
        full_body_3 = db.session.query(Full_Body_Three).get(1)

        # getting the full body 4 Day exercises from the table in the database
        full_body_4_exercises = text("SELECT exercise1, exercise2, exercise3, exercise4, exercise5 FROM Full__Body__One_4day ")
        full_body_4_result = db.session.execute(full_body_4_exercises).fetchall()

        full_body4_1 = db.session.query(Full_Body_One_4day).get(1)
        full_body4_2 = db.session.query(Full_Body_Two_4day).get(1)
        full_body4_3 = db.session.query(Full_Body_Three_4day).get(1)
        full_body4_4 = db.session.query(Full_Body_Four_4day).get(1)

        # getting the uppper/lower-full body 5 day exercises from the table in the database
        ul_ppl_5_exercises = text("SELECT exercise1, exercise2, exercise3, exercise4, exercise5 FROM UL_PPL__One ")
        ul_ppl_5_result = db.session.execute(ul_ppl_5_exercises).fetchall()

        ul_ppl_1 = db.session.query(UL_PPL_One).get(1)
        ul_ppl_2 = db.session.query(UL_PPL_Two).get(1)
        ul_ppl_3 = db.session.query(UL_PPL_Three).get(1)
        ul_ppl_4 = db.session.query(UL_PPL_Four).get(1)
        ul_ppl_5 = db.session.query(UL_PPL_Five).get(1)

        # getting the full body 2 day exercises from the table in the database
        ul_exercises = text("SELECT exercise1, exercise2, exercise3, exercise4, exercise5 FROM Upper_2day ")
        ul_result = db.session.execute(ul_exercises).fetchall()

        ul_upper = db.session.query(Upper_2day).get(1)
        ul_lower = db.session.query(Lower_2day).get(1)

        return render_template('workouts.html', user=current_user, upper_one=upper_1, lower_one=lower_1,
                                upper_two=upper_2, lower_two=lower_2, upper_three=upper_3, lower_three=lower_3, full_body_one=full_body_1,
                                full_body_two=full_body_2, full_body_three=full_body_3, full_body4_one=full_body4_1, full_body4_two=full_body4_2,
                                full_body4_three=full_body4_3, full_body4_four=full_body4_4, ul_ppl_one=ul_ppl_1,ul_ppl_two=ul_ppl_2, ul_ppl_three=ul_ppl_3,
                                ul_ppl_four=ul_ppl_4, ul_ppl_five=ul_ppl_5, ul_upper=ul_upper, ul_lower=ul_lower, upper_one_result=upper_one_result,
                                full_body_3_result=full_body_3_result, full_body_4_result=full_body_4_result, ul_ppl_5_result=ul_ppl_5_result,
                                ul_result=ul_result) 