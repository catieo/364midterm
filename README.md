# 364midterm

Midterm Assignment for SI 364. <br>
Catie Olson 

Requirements to complete for 1800 points (90%) -- an awesome, solid app
(I recommend treating this as a checklist and checking things off as you get them done!)

Documentation Requirements (so we can grade the assignments)
Note: See To Submit for submission instructions.
Create a README.md file for your app that includes the full list of requirements from this page. The ones you have completed should be bolded. (You bold things in Markdown by using two asterisks, like this: **This text would be bold** and this text would not be)
The README.md file should include a list of all of the routes that exist in the app and the names of the templates each one should render (e.g. /form -> form.html, like the list we provided in the instructions for HW2).
The README.md file should contain at least 1 line of description of what your app is about or should do.
Code Requirements
Note that many of these requirements go together!
<br>
**Ensure that the SI364midterm.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up)** <br>
**Add navigation in base.html with links (using a href tags) that lead to every other viewable page in the application.** <br>
**Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.** <br>
**Include at least 2 additional template .html files we did not provide.** <br>
**At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.** <br>
**At least one errorhandler for a 404 error and a corresponding template.** <br>
**At least one request to a REST API that is based on data submitted in a WTForm.** <br>
**At least one additional (not provided) WTForm that sends data with a GET request to a new page.**  <br>
**At least one additional (not provided) WTForm that sends data with a POST request to the same page.** <br>
**At least one custom validator for a field in a WTForm.** <br>
**At least 2 additional model classes.** <br>
**Have a one:many relationship that works properly built between 2 of your models.** <br>
**Successfully save data to each table.** <br>
**Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).** <br>
**Query data using an .all() method in at least one view function and send the results of that query to a template.** <br>
**Include at least one use of redirect.** <br>
**Include at least one use of url_for.** <br>
**Have at least 3 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of base.html.)** <br>
Additional Requirements for an additional 200 points (to reach 100%) -- an app with extra functionality! <br>
**(100 points) Write code in your Python file that will allow a user to submit duplicate data to a form, but will not save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3).**<br>
