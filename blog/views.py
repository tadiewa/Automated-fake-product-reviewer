from django.shortcuts import render, redirect,get_object_or_404
from blog.models import BlogPost , comment
from blog.forms import CreateBlogPostForm,commentForm
from django.db.models import Count
from account.models import Account
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit
import random
from home.views import fakepage_view
from account.views import logout_view
from .review_classifer import classify_review

## dataset
dataset = pd.read_csv('C:/Users/TADIWA/final/finale/finale/dsetq2.csv')
data = dataset.copy()

##spliting data into training set and test set
## Since the majority of reviews are positive (5 stars), 
#there is need to do a stratified split on the reviews score to ensure that we don't train the classifier on imbalanced data
#To use sklearn's Stratified ShuffleSplit class, 
#i'm going to remove all samples that have NAN in review score, then covert all review scores to integer datatype



dataAfter = data.dropna(subset=["reviews.rating"]) # removes all NAN in reviews.rating
dataAfter["reviews.rating"] = dataAfter["reviews.rating"].astype(int)
split = StratifiedShuffleSplit(n_splits=5, test_size=0.2)
for train_index, test_index in split.split(data, data["reviews.rating"]): 
    data_train = data.reindex(train_index)
    data_test = data.reindex(test_index)

def sentiments(rating):
    if (rating == 5) or (rating == 4):
        return "Positive"
    #elif rating == 3:
       # return "Neutral"
    elif (rating == 2) or (rating == 1) or (rating == 3):
        return "Negative"
# Add sentiments to the data





def create_blog_view(request):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateBlogPostForm(request.POST or None , request.FILES or None)
    if form.is_valid():
        obj = form.save(commit = False)
       


        author = Account.objects.filter(email=user.email).first()
        obj.author = author
         
        obj.save()
        form = CreateBlogPostForm()

    context['form'] = form 
     


    return render(request, "blog/create_blog.html", context)

def detail_blog_view(request ,slug ):

    blog = get_object_or_404(BlogPost,slug=slug)
    blog_name = blog.title
    displaycomment =  comment.objects.filter(post=blog_name).order_by('-id')[:3]
    comments =  comment.objects.filter(post=blog_name)
    postupdates = BlogPost.objects.all()[:5]
    number = comments.count()


   


    
    if request.method=="POST":
        form =  commentForm(request.POST)
        if form.is_valid():
            OBJ= form.save(commit=False)
            text = form.cleaned_data.get("content")
            classifier =  classify_review(text)
            print(classifier)
            content = []
            content.append(text)
            comments =  comment.objects.filter(post=blog_name)
            commentsuser = comment.objects.filter(author = request.user)
            commentsuserspecific = comment.objects.filter(author = request.user,post=blog_name)
            usercommentspecific = commentsuserspecific.count()
            print("hhhh:", usercommentspecific)
            rating= form.cleaned_data.get("rating")
            print("rating number:",rating )
            number = comments.count()
            usercomment_number = commentsuser.count()
            target = ['negative' , 'positive']
            
            print("xxx:", usercomment_number)
            ## count all blogposts
            blogpostcount = BlogPost.objects.count()
           
            if usercommentspecific > 3:
                return redirect('commentnumber')
            ##if total blogposts and total user commenets are equal delete user and  label fake
            if blogpostcount >5 and blogpostcount <= usercomment_number:
                print("robot fake")
                Account.objects.filter(username=request.user).delete()
                return redirect('Robot')
               
            if target[classifier[0]]=="positive" and int(rating) <= 3:
                return redirect('fakepage')
            elif target[classifier[0]]=="negative" and int(rating) > 3:
                return redirect('fakepage')
            else:
                print("geniune")
               
            ## check number of posts by the user
            if usercomment_number >= 3:
             
                OBJ.author = request.user
                OBJ.status = target[classifier[0]]
                ptk = OBJ.status
                print("###:", ptk)
                OBJ.post= blog_name
                OBJ.rating =rating

                
                
                # poscom  = comment.objects.filter(post=blog_name,status__contains="Positive")
                #posnum = poscom.count()
                #negcom  = comment.objects.filter(post=blog_name,status__contains="Negative")
                #negnum = negcom.count()

                ## cosine similarity
                
                all_comments =[]
                same_author_comments = comment.objects.filter(author = request.user)
                for item in same_author_comments:
                    all_comments.append(item.content)


                sentence = ""
                ## randomise and concatenate word in list
                #print("Pick 5 Random element from list:",random.sample(all_comments,5))
                for td in range(5):
                    # print (''.join(random.sample(all_comments,5)))
                    n = random.randint(0,len(all_comments)-1)
                    sentence +=" "+all_comments[n]
                print(sentence)

                index = [sentence, text]
                    
                #tfidf_transformer = TfidfTransformer(stop_words='english')
                count_vectorizer = CountVectorizer(stop_words='english')
                count_vectorizer = CountVectorizer() 
                #tfidf_transformer = TfidfTransformer()
                
                sparse_matrix = count_vectorizer.fit_transform(index)
                #sparse_matrix = tfidf_transformer.fit_transform(index)

                # for px in range(len(all_comments)):
                    # index.append(px)


                    
                doc_term_matrix = sparse_matrix.todense() 
                df = pd.DataFrame(doc_term_matrix,                  
                                columns=count_vectorizer.get_feature_names(),                   
                                index= index) 

                
                print("hhh",cosine_similarity(df))
                #df.values.tolist()
                x = cosine_similarity(df)[1][0]

                print("hhh",x)

                if  x >= 0.5:
                    print ("fake")
                    
                else:
                    print("geniune")
                    OBJ.save()
                    number = comments.count()

                 

            else:
                
                OBJ.author = request.user
                OBJ.status = target[classifier[0]]
                pj = OBJ.status
                print("###hh:",pj)
                OBJ.post= blog_name
                OBJ.save()
                number = comments.count()

                
                    
                
    form = commentForm()  

    
    blog_post = get_object_or_404(BlogPost, slug=slug )
    
    

    return render(request, 'blog/detail_blog2.html' , {'blog_post':blog_post,"form":form,'comments':comments, 'number':number,'blogpost':postupdates,'displaycomment':displaycomment})

 


