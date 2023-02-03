# This program will take the user's input on a few questions to determine what type of workout split they want. It also using the calorie calculator program to determnine 
# what exercises, how many exercises and how many days to workout.


#from .calorie_calculator import weight, gender, height, age
from random import randint

# creating a list of exercises for each workout day 
hor_push_exercises = [ 'bench', 'db bench',  'lateral raises', 'cable flys', 'pushups', 'pec deck']
vert_push_exercises = ['overhead shoulder press', 'arnold press', 'dips', 'db shoulder press']
hor_pull_exercises = ['bent rows', 'cable rows', 'chest supported row' ]
vert_pull_exercises = ['pullups', 'pull downs', 'lat prayers']
quad_exercises = ['back squat', 'leg press', 'leg extension', 'front squat']
ham_exercises = ['rdl', 'db rdl', 'leg curl', 'single leg squat']
arm_exercises = ['overhead tri extension', 'tri rope push downs', 'db curl', 'db hammer curl', 'rope curl', 'skull crushers']

# creating the method for push, legs, pull routine
def push_legs_pull():
    # creating a list of days to assign exercises to

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    exercise_days = ['push1', 'legs1', 'pull1', 'push2', 'legs2', 'pull2', 'rest']
    # pairing each day with a specific exercise movement for that day
    exercise_day_and_day = dict(zip(days, exercise_days))
    print('Here are your muscle groups for each day: ',exercise_day_and_day)

    # pull 2 vertical and horizontal push exercises and 1 arm exercise from the list of exercises
    # Push 1

    push_one = []
    i = 0
    # getting 2 horizontal push exercises
    while i < 2:
        if hor_push_exercises[randint(0,len(hor_push_exercises)-1)] != push_one[0:2]:
            push_one.append(hor_push_exercises[randint(0,len(hor_push_exercises)-1)])
        i = i+1

    # getting 2 vertical push exercises
    while i < 4:
        if vert_push_exercises[randint(0,len(vert_push_exercises)-1)] != push_one[2:4]:
            push_one.append(vert_push_exercises[randint(0,len(vert_push_exercises)-1)])
        i = i+1
    
    # getting 1 arm exercise 
    while i < 5:
        if arm_exercises[randint(0,len(arm_exercises)-1)] != push_one[4:5]:
            push_one.append(arm_exercises[randint(0,len(arm_exercises)-1)])
        i = i+1

    # Legs1 will go here, copy the same structure as above
    
    legs_one = []
    j = 0
    # getting 2 quad exercises
    while j < 2:
        if quad_exercises[randint(0,len(quad_exercises)-1)] != legs_one[0:2]:
            legs_one.append(quad_exercises[randint(0,len(quad_exercises)-1)])
        j = j+1

    # getting 2 ham exercises
    while j < 4:
        if ham_exercises[randint(0,len(ham_exercises)-1)] != legs_one[2:4]:
            legs_one.append(ham_exercises[randint(0,len(ham_exercises)-1)])
        j = j+1
    
    # getting 1 arm exercise 
    while j < 5:
        if arm_exercises[randint(0,len(arm_exercises)-1)] != legs_one[4:5]:
            legs_one.append(arm_exercises[randint(0,len(arm_exercises)-1)])
        j = j+1

    #Pull 1

    pull_one = []
    k = 0
    # getting 2 horizontal pull exercises
    while k < 2:
        if hor_pull_exercises[randint(0,len(hor_pull_exercises)-1)] != pull_one[0:2]:
            pull_one.append(hor_pull_exercises[randint(0,len(hor_pull_exercises)-1)])
        k = k+1

    # getting 2 vertical pull exercises
    while k < 4:
        if vert_pull_exercises[randint(0,len(vert_pull_exercises)-1)] != pull_one[2:4]:
            pull_one.append(vert_pull_exercises[randint(0,len(vert_pull_exercises)-1)])
        k = k+1
    
    # getting 1 arm exercise 
    while k < 5:
        if arm_exercises[randint(0,len(arm_exercises)-1)] != pull_one[4:5]:
            pull_one.append(arm_exercises[randint(0,len(arm_exercises)-1)])
        k = k+1



    print('Push1:',push_one)
    print('Legs1:',legs_one)
    print('Pull1:',pull_one)
 


    


# creating the method for the full body routine
def full_body():
    pass

#creating the method for the upper/lower routine    
def upper_lower():
    pass

# getting user input based on the workout split they want to do
def get_user_input():
    while True:
        while True:
            workout_split = str(input('What type of workout split would you like? (Push, Legs, Pull; Full Body; Upper/Lower)'))
            if workout_split in ('Push, Legs, Pull', 'Full Body', 'Upper/Lower'):
                break
            print("Please enter a valid selection")
        if workout_split == 'Push, Legs, Pull':
            push_legs_pull()
        elif workout_split == 'Full Body':
            full_body()
        elif workout_split == 'Upper/Lower':
            upper_lower()
        else:
            print('Please enter a valid workout split.')

def main(): 
    get_user_input()
       

if __name__ == '__main__':
    main()