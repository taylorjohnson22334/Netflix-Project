#To run this program you will need to have pandas, numpy, bs4, requests, and re installed.
import pandas as pd, numpy as np, bs4, requests, re
pd.options.mode.chained_assignment = None

#The data used in this project is from a Kaggle dataset named Netflix Movies and TV Shows, posted by Shivam Bansal.
#You will need to download this dataset and change the pathway below to run this code.

netflix_titles = pd.read_csv('C:\\Users\\taylo\\Data Science Materials\\netflix_titles.csv')

#The first section of this code filters the original dataframe based on the user's preference of movies or tv shows.
#It also creates label_string which will be used throughout the rest of the code to ask the user questions.

while True:
    print('Are you interested in a movie or a tv show?')
    answer = input()
    if answer.lower() == 'tv show':
        label_string = 'TV Shows'
        df = netflix_titles['type'] == 'TV Show'
        df = netflix_titles[df]
        break
        
    if answer.lower() == 'movie':
        label_string = 'Movies'
        df = netflix_titles['type'] == 'Movie'
        df = netflix_titles[df]
        break

#This section cleans the genre column in the dataframe and makes it easier for users to access their preferred genre or genres.
#This section introduces the genre_list and genre_list_unique lists. genre_list will be used to catalog the genres of each
#movie or tv show in the dataframe and be iterated through to clean up each genre and make it more user-friendly. genre_list_unique
#will catalog each unique genre in the dataframe and be used later as a guide if the user would like a list of available genres to choose from.

genre_list = []
genre_list_unique = []
remove_words = ['TV Shows', 'TV Show', 'TV', 'Movies', 'Movie']
for i in range(len(df)):
    genres = str(df.iloc[i, 10]).split(',')
    genre_list.append(genres)

#The main goal of cleaning up the genres column is to make it more user friendly. The main issue comes when two genres are listed simultaneously.
#When two genres are listed simultaneously, this upcoming for loop will convert both to a singular form.

#A good example of why it is important to do this is in the case of documentaries. On Netflix, documentaries are listed as a specific
#subgenre + "documentaries" (sports documentaries, nature documentaries, etc.). If a user was asked to enter what genre they preferred
#and entered 'documentary' the original dataframe wouldn't account for a large portion of specialized documentaries. If we change
#documentaries to the singular form documentary, our program will be able to select all forms of documentaries rather than specific instances.

#Another example of why it is important to do this is in the case of genres such as romantic comedies. Ideally, we would like romantic
#comedies to show up when users select romance or comedy movies. If a user was asked to enter what genre they preferred and entered
#'romance' or 'comedy' romantic comedies would not show up in their selection. If we change romantic comedies to romance comedy the
#movie or tv show will be properly selected when the user enters their preferred genre.
    
for i in range(len(genre_list)):
    for j in range(len(genre_list[i])):
        for word in remove_words:
             if word in genre_list[i][j]:
                genre_list[i][j] = genre_list[i][j].replace(word, '')
        if genre_list[i][j].endswith('ies') and 'series' not in genre_list[i][j].lower():
            genre_list[i][j] = genre_list[i][j].replace('ies', 'y')
        if genre_list[i][j].endswith('s') and genre_list[i][j] != 'Sports' and 'series' not in genre_list[i][j].lower():
            genre_list[i][j] = genre_list[i][j][:-1]
        if genre_list[i][j].endswith('antic '):
            genre_list[i][j] = genre_list[i][j].replace('antic ', 'ance')
        if genre_list[i][j].endswith('\' '):
            genre_list[i][j] = genre_list[i][j][:-2]
    genre_list[i][j] = genre_list[i][j].strip()
    if genre_list[i][j].strip() not in genre_list_unique:
        genre_list_unique.append(genre_list[i][j].strip())
for i in range(len(df)):
    string = ' '.join(genre_list[i])
    df.iloc[i, 10] = string

#The goal of this upcoming for loop is to clean up genre_list_unique and split up indices with two or more genres. Once we do
#this we will be able to show the user all available genres to select from if they are curious.
    
for i in range(len(genre_list_unique)):
    if '&' in genre_list_unique[i]:
        genres = genre_list_unique[i].split('&')
        if genres[0].strip() not in genre_list_unique and genres[1].strip() not in genre_list_unique:
            genre_list_unique[i] = genres[0].strip()
            genre_list_unique.append(genres[1].strip())
        if genres[0].strip() not in genre_list_unique and genres[1].strip() in genre_list_unique:
            genre_list_unique[i] = genres[0].strip()
        if genres[0].strip() in genre_list_unique and genres[1].strip() not in genre_list_unique:
            genre_list_unique[i] = genres[1].strip()

#57% of the movies and tv shows in this dataset are international. Below I give the user the option to filter out that content.

while True:
    print('Would you like to filter out International ' + label_string + '?')
    answer = input()
    if answer.lower() == 'yes':
        indices = []
        for i in range(len(df) - 1):
            if 'United States' in str(df.iloc[i, 5]):
                indices.append(i)
        df = df.iloc[indices]
        break
    if answer.lower() == 'no':
        break

#The show_id column is redundant in our dataframe so we remove it.

del df['show_id']    

#This upcoming section allows the user to enter their preferred genre and filters the dataset based on their selection. If a user
#would like more than one genre to be in the selection they can enter multiple genres separated by commas. If a user doesn't have
#a preferred genre they can hit enter to select all genres. The most important variable in this section is key. key starts off
#being equal to 0 and if the entered genre is valid it will stay 0, break the while True condition, and continue on to the next
#section. If the entered genre is not valid, key will become equal to 1. When this happens the program informs the user that their
#preferred genre is not valid. From here the user can either enter another genre or see a list of available genres to choose from.

while True:
    print('Enter the genre you are interested in:')
    print('If you are interested in more than one, separate them by a comma.')
    print('If you aren\'t interested in a specific genre, hit enter.')
    key = 0
    answer = input()
    
    if ',' in answer:
        answer_split = answer.split(',')
        for genre in answer_split:
            if genre.title().strip() in genre_list_unique:
                continue
            else:
                print('The genre you entered, ' + genre.title().strip() + ', is not valid.')
                key = 1
                break
    else:
        if answer.title().strip() in genre_list_unique:
            break
        else:
            key = 1
            print('The genre you entered, ' + answer.title().strip() + ', is not valid.')
            
    if key == 1:
        while True:
            print('Would you like a list of availible genres?')
            answer = input()
            if answer.lower() == 'yes':
                string = ''
                for genre in genre_list_unique[:-1]:
                    string += genre + ', '
                string += 'and ' + genre_list_unique[-1]
                print(string)
                break
            if answer.lower() == 'no':
                break
    if key == 0:
        break

#This if statement only concerns cases where a user enters multiple genres. The user has the option to have this selection be inclusive or exclusive.
#If the user enters inclusive and enters 'comedy, drama' the program will select movies or tv shows that are comedies or dramas, if the user enters
#exclusive and enters 'comedy, drama' the program will select movies or tv shows that are both comedies and dramas. If the user doesn't know what these
#terms mean they can enter 'explanation' and have the words defined for them.

if ',' in answer:
    genre_df_dict = {}
    answer_split = answer.split(',')
    for genre in answer_split:
        indices = []
        for i in range(len(df) - 1):
            if genre.title() in df.iloc[i, 9]:
                indices.append(i)
        df = df.iloc[indices]
        genre_df_dict[genre.strip() + '_df'] = df
    lst = [key for key in genre_df_dict.keys()]

    while True:
        print('Would you like these genres to be inclusive or exclusive?')
        print('If you would like an explanation of these terms, type explanation.')
        answer = input()
        if answer.lower() == 'explanation':
            print('Exclusive would mean that if you enter (comedy, drama),' + label_string + ' selected will be both comedies and dramas.')
            print('Inclusive would mean that if you enter (comedy, drama),' + label_string + ' selected will be comedies or dramas.')
        if answer.lower() == 'inclusive':
            if len(lst) == 2:
                df = pd.merge(genre_df_dict[lst[0]], genre_df_dict[lst[1]], how = 'outer')
            if len(lst) == 3:
                df = pd.merge(genre_df_dict[lst[0]], genre_df_dict[lst[1]], how = 'outer')
                df = pd.merge(df, genre_df_dict[lst[2]], how = 'outer')
            break

        if answer.lower() == 'exclusive':
            if len(lst) == 2:
                df = pd.merge(genre_df_dict[lst[0]], genre_df_dict[lst[1]], how = 'inner')
            if len(lst) == 3:
                df = pd.merge(genre_df_dict[lst[0]], genre_df_dict[lst[1]], how = 'inner')
                df = pd.merge(df, genre_df_dict[lst[2]], how = 'inner')
            break

#This else statement only concerns cases where a user enters one genre. This is a very straightforward process where the program will
#search through the genre column in the dataset and select movies or tv shows that contain the preferred genre.

else:
    indices = []
    for i in range(len(df)):
        if answer.title() in df.iloc[i, 9]:
            indices.append(i)
    df = df.iloc[indices]

#This next section allows the user to enter actors or actresses that they would like to see in their selection. It first asks the user
#if they would like to use this feature. If they would like to do so they are asked to enter their preferred actor or actress. Just like in
#the genre section if they prefer more than one they can enter as many as they like separated by commas. The program goes through the cast
#column in the dataframe ad identifies movies or tv shows that contain the desired cast member(s). If no movies or tv shows contain the
#desired cast member(s) or if there is a spelling error the program will take the user back to the initial question.

while True:
    print('Are there any actors or actresses you would like to see in your selection?')
    print('Enter yes or no.')
    answer = input()
    if answer.lower() == 'yes':
        print('Enter the actor or actress you are interested in.')
        print('If you are interested in more than one, type them out separated by a comma.')
        cast_preference = input().lower()

        cast_list = [str(df.iloc[i,3]).split(',') for i in range(len(df))]

        indices = []
        for i in range(len(cast_list)):
            for cast_member in cast_list[i]:
                if cast_member.strip().lower() in cast_preference:
                    indices.append(i)

        new_df = df.iloc[indices]
        if len(new_df) > 1:
            df = new_df
            break
        else:
            print('There are no ' + label_string + ' in your chosen genre with ' + cast_preference)
            print('Make sure you have correct spelling, or change your selection to find another Actor/Actress')

    if answer.lower() == 'no':
        break

df.reset_index(inplace = True, drop = True)

#The goal of this program is to help users make a selection on a movie or tv show based on their preferences. Once all the users
#preferences have been entered the program randomly selects 3 movies or tv shows from the data frame to print out for the user. If the
#length of the dataframe is less than 3 the program will print out every movie in the dataframe. Along with the title, description, and year
#attributes from the dataframe, the program will also use google to find critics and audience reviews from imdb and rotten tomatoes respectively
#and print them out as well.
                                                      
if len(df) >= 3:
    final_list = df.sample(3)
else:
    final_list = df

for i in range(len(final_list)):
    year = str(final_list.iloc[i,6])
    title = str(final_list.iloc[i, 1])
    title = title.replace(' ', '_').lower()
    if '&' in title:
        title = title.replace('&', 'and')
    remove_chars = ['\'', ':', '.', '!', '-', ',']
    for char in title:
        if char in remove_chars:
            title = title.replace(char, '')

    critics_consensus = 'N/A'
    audience_score = 'N/A'

    page = requests.get('https://www.google.com/search?q=' + title.replace('_', '+') + '+' + year)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')

    rating_tags = soup.find_all('div', {'class':re.compile(r'^(BNeawe)')})
    ratings = [tag.getText() for tag in rating_tags]
        
    ratings_string = ''
    for j in range(len(ratings)):
        if 'Rotten Tomatoes\n' in ratings[j] and 'IMDb\n' in ratings[j]:
            ratings_list = ratings[j].split('IMDb\n')
            if '/' in ratings_list[0] and '%' in ratings_list[0]:
                ratings_list = ratings_list[0].split('Rotten Tomatoes\n')
                critics_consensus = ratings_list[0][:3]

                audience_score = ratings_list[1][:6]
                audience_score = audience_score.split('/')
                audience_score = str(int(float(audience_score[0]) * 10)) + '%'
                break

            if '/' in ratings_list[0]:
                critics_consensus = ratings_list[1][:3]
                audience_score = ratings_list[0][:6]
                audience_score = audience_score.split('/')
                audience_score = str(int(float(audience_score[0]) * 10)) + '%'



        if 'Rating' in ratings[j]:
            ratings_split = ratings[j].split('Rating  ')
            if '%' not in ratings[j] and '/' not in ratings[j]:
                break
            if '%' in ratings_split[0][:3]:
                critcs_consensus = ratings_split[0][:3]
                break
                
            audience_score = ratings_split[1][:6]
            audience_score = audience_score.split('/')
            audience_score = str(int(float(audience_score[0]) * 10)) + '%'
            break

        if 'IMDb\n' in ratings[j]:
            audience_score = ratings[j][:6]
            audience_score = audience_score.split('/')
            audience_score = str(int(float(audience_score[0]) * 10)) + '%'
    
    print(str(final_list.iloc[i,1]) + '\n' + str(final_list.iloc[i,10]) + '\n' + str(final_list.iloc[i,6]) + ' ' + str(final_list.iloc[i,7])
            + ' ' + str(final_list.iloc[i,8]) + ' ' + str(final_list.iloc[i,9]) + '\n' + 'Critics Consensus: ' + critics_consensus
            + ' Audience Score: ' + audience_score + '\n')



