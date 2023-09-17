# Parsite
#### Video Demo:  https://youtu.be/CLWLUuKzHLk
#### Description:

## Project description

The main idea of this project is to help people find apartments much faster by collecting ads from different websites info one database. To do this, I have created 3 different classes using Python (in "parsing/main.py") for such websites as Avito, Domclick, Cian in which I used Selenium, Beautifulsoup, Requests, Json  libraries, therefore I have parsed relevant information from every page and added key information to database. 

By using this script all these functions are performed automatically. During the process I faced several problems. For instance, 403 error and defence system, but I was able to fix it, as a result chrome launches not like a software but as a real user. However,  it was really difficult to access to Domclick website, therefore I couldn't have parsed it yet. Once a week table from this database constantly updating. From the user perspective, when the user fill the query form such as filters, he gets relevant information from all 3 websites.

All advertisement cards contain id, link, title, price, address, metro station, description, image, website columns and the "query_result" page demonstrates these cards with these information.

<b>My project is made only for informational purpose, it shows  a post template with a link to the original page of the website</b>. By clicking the link you will be directed to the original page on definite website.

Another main option is created ads page: user who logged in has an opportunity to make his/her own posts (e.x. car or apartment advertisement).
After creating, on the main page you will be able to see these posts which you or someone else created.
Client can also add advertisement to favorite by clicking "heart" symbol at the right top corner and delete them by clicking the same button but at the <b>favorite page</b>.

In addition, user have their own page (profile) named "account" where user's and whole site's information are demonstrated.

This system is not created for commercial using but only as an educational and informational example of software.





## detailed analysis of app.py functions
### index: 
Acts as a main page which contains advertisements created on my website.

<ul>
Relevant files: 
<li>index.html - inherited from layout.html, displays advertisements</li>
<li>style_index.css - stylesheet for index.html</li>
<li>Table in database called 'apartments' where ads information is sourced</li>
</ul>

### query:
Acts as a filter where users can select relevant options and data fot discovering advertisements from Avito, Domclick or Cian.  
<ul>
Relevant files: 
<li>query.html</li>
<li>style_query.css</li>
<li>In app.py file send a request to the 'query_result' using sqlite3 queries</li>
</ul>

### query_result: 
Acts similar to index but with different advertisements. All data sourced from other websites (Avito, Cian, Domclick), which depends on selected options
<ul>
Relevant files:
<li>query_result.html</li>
<li>style_query_result.html</li>
<li>"cian_aps" table where ads from Cian website is sourced</li>
<li>"dom_aps" table where ads from Domclick website is sourced</li>
<li>"avito_aps" table where ads from Avito website is sourced</li>
<li>In app.py file it gets queries from 'query page' and selects relevant information</li>
</ul>

### favorite | add_to_favorites | remove_from_favorites:
Contains ads which were selected as "Liked" or "Favorites" by clicking "heart" button on the index page. And the opposite action happens on "favorite" page using the same method.
<ul>
Relevant files:
<li>favorite.html</li>
<li>style_favorite.html</li>
<li>"users_fav" table which contains favorite advertisements</li>
<li>In app.py it gets the id of ad from index page after clicking "heart" button and displaces on "favorite" page</li>
</ul>


### create:
It is displaced as a create form where users input such data as title, price, address, etc. And it records these data to the "apartments" table in database.
<ul>
Relevant files:
<li>create.html</li>
<li>style_create.html</li>
<li>In app.py it sends data to the database ("apartments" table)</li>
</ul>


### login:
It acts as a simple login form with "login" and "password" blocks.
<ul>
Relevant files:
<li>login.html</li>
<li>style_login.html</li>
<li>In app.py it selects user data from the database ("users" table)</li>
</ul>

### register:
It acts as a simple register form with "name", "surname", "mail", "login" and "password" blocks.
<ul>
Relevant files:
<li>register.html</li>
<li>style_register.html</li>
<li>In app.py it sends user data to the database ("users" and "user_info" tables)</li>
</ul>


### logout

### account | edit_account
This is an user's page where user's and site's information are displaced
<ul>
Relevant files:
<li>account.html</li>
<li>style_account.html</li>
<li>main_account.js</li>
<li>In app.py it selects data from ALL tables and displaces it</li>
<li>edit_account function allows to change user's data</li>
</ul>











