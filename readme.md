E-commerce Website
====================

This is an E-commerce website developed mainly to focus on Django following along the ***justdjango*** channel. I used a free template from [mdbootstrap](https://mdbootstrap.com/snippets/jquery/mdbootstrap/50504?action=full_screen_mode) and developed most common features that an usual E-commerce website contains. I wrote both ***generic class based*** and ***functional*** views in the backend. The database I am using is the default django's ***Sqlite***. Another interesting thing was using the ***Stripe Api*** for handling the payment process.

I have also deployed the project on [pythonanywhere.com](http://nabil.pythonanywhere.com/). The project can be viewed live on this domain ***nabil.pythonanywhere.com***

Here I am noting down some of the features below and I will instruct you through the process to this run this project on your local machine if you are interested.




Features
====================
+ User Authentication & Management Using ***django-allauth***
+ Filtering & Searching Items By Category
+ Adding & Removing Items From/To The Cart
+ Add Likes To Product
+ Cart Management
+ Adding Coupons While Ordering To Cut Down Price
+ Commercial & User Friendly Checkout Process Using Dynamic Form
+ Handling Payment Using ***Stripe*** Api Gateway
+ Order History
+ Request Refund
+ Customized Default Django Admin Dashboard

Directory Layout
====================

Django E-commerce Website App's directory structure looks as follows::

    E-commerce-Website-Django/
        |---core
        |--djangoecommerce
        |---static
        |---static_in_env
        |---templates
        |---.env
        |---manage.py
        |---.gitignore
        |---requirements.txt
        |----readme.md

Suggestion
====================

I recommend you to have ***python >= 3.6*** installed on your machine to use this app. BTW I have used the version ***python 3.8*** though :)

# Usage

First clone this repo and go to the project root.

    $ git clone https://github.com/MoinulHossainNabil/E-commerce-Website-Django.git
    $ cd E-commerce-Website-Django

I would recommend to work on a virtual environment. I have used ***virtualenv*** package to create a virtual environment you may wanna use other package. So install this as well if you already haven't.

    $ pip install virtualenv
    $ ls
    
You will see the following directory and files:

    core/   djangoecommerce/    static/  static_in_env/ templates/  requirements.txt
    db.sqlite3  manage.py   readme.md
    
Now create you own virtual environment here and install the project required packages written in requirements.txt file by running the following commands.

    $ virtualenv venv_name

Activate the virtual environment by the following command:

***On Windows***
    
    $ source venv_name/Scripts/activate  # Using Git Bash
    
***On Linux***

    $ source venv_name/bin/activate
    
Now install the package requirements by:

    $ pip install -r requirements.txt
    
Well your environment is ready now.

Getting Started
====================

Finally, you have to make migrations to get the app started and create a new superuser to interact with the admin dashboard.
So run the following commands as follows:

    $ python manage.py migrate
    $ python manage.py createsuperuser --user <username> --email <email>

So after successful completion of these you are ready to run the application by the following command:

    $ python manage.py runserver
    
Static Files
====================

Well, I have configured the settings.py to use all the static files. Hopefully, you will have the UI properly. But if you don't see the styling work, just run the following command:

    $ python manage.py collectstatic
   
Now open the browser go to ***localhost/8000/*** and you will see the home page of the application.
But you will find no product. Because you have to add items by login to the the admin dashboard using the username and password you created as a super user.
So login to the admin panel using ***localhost:8000/admin/*** and you will find all of the models used so far as noted below.

Models
====================

+ UserProfile
+ Item
+ Category
+ OrderItem
+ Cart
+ Address
+ Payment
+ Coupon
+ Refund
+ Comment

Add some items to the ***Item*** model in the admin then you can make your hands dirty with the app. Well I have paginated the home page by ***8*** currently. So, have to add at least more than 8 items to see the pagination functionality.

Stripe
====================
I have used ***Stripe*** for handling payment of the order. Stripe officially provides card numbers for the testing purpose of their API's. So use  ***Card Number 4242 4242 4242 4242*** and specify a future a date like ***12/30*** in MM while filling up the payment form for an order to make.

Deployment
====================

As I have mentioned firstly, the project in deployed on [pythonanywhere.com](http://nabil.pythonanywhere.com/) with free hosting facility and can be viewed live on this domain ***nabil.pythonanywhere.com***
