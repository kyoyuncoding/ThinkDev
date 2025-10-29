# ThinkDev.
#### Video Demo: <URL https://www.youtube.com/watch?v=Faxf1cHATKQ&t=1s>
#### Description: 

ThinkDev is a structured journal, allowing users to systematically approach programming problems to reach and store effective solutions.

I created this web app using Django and Bootstrap, utilizing a combination of languages such as Python, HTML, and CSS. I decided to use the Django framework as it was one that I had gained some level of familiarity with through the CS50w course, and I decided to use Bootstrap as I particularly liked the main Bootstrap text font.

When I approached different programming problems, such as LeetCode or real world problems, and attempted to use best practices such as writing pseudo-code, and whiteboarding the problem before writing source code, my documentations of these problems were scattered and not easily referred back to or accessed. It got to the point that the friction I experienced whilst attempting to apply these best practices was so great, I would rather attempt to solve the problem directly, rather than having to sift through different Google Docs files, and scrolling endlessly, to refer back to problems that I had been working on for multiple sessions.

My project attempts to solve this problem by allowing users to structure their thoughts when approaching a problem, prompting users to first write down in natural language their understanding of the problem, then to write out their thoughts in pseudo-code, before translating the pseudo-code into source code. These problems can then be saved, accessed, edited, and deleted. The past versions of each problem can also be viewed. I believe that by consistently approaching problems in this way, whilst being able to easily store and access thoughts, users' general problem-solving skills will be strengthened, and users will be encouraged to think about a problem extensively, before attempting to code a solution.

#### Project Files:

thinkdev/problemlog/static/styles.css - This file contains all of my CSS rules to help format my webapp pages.

thinkdev/problemlog/static/home-layout.html - This file contains the home page HTML template which is extended to all pages where the user has not logged in i.e, the login, register, and home page.

thinkdev/problemlog/static/index.html - The home page. Consists of the upper navigation menu, and the ThinkDev text in the middle of the screen.

thinkdev/problemlog/static/register.html - Allows users to register an account for the webapp. If a parameter is not entered (such as the email address) or the password confirmation does not match, or there is already an existing account using the email or username, a relevant error message is thrown up on screen.

thinkdev/problemlog/static/login.html - Allows users to log in to the webapp. If the username and password details are incorrect, an error message is thrown up on the screen.

thinkdev/problemlog/static/layout.html - The HTML template page for all pages after logging in. Uses CSS-grid to create a black sidebar, and also contains the navigation links to create a new problem, browse previously saved problems, and log out.

thinkdev/problemlog/static/problem-log.html - The HTML file that contains the main problem log page. Consists of structured prompts, text areas, and a dropdown menu to confirm whether or not the problem is solved or not.

thinkdev/problemlog/static/log.html - The HTML file that contains the previously saved problems page. Consists of all saved problems. Shows the date of creation, an edit button to allow you to edit the problem entry, a delete button to allow you to delete the problem entry, whether or not the problem is marked as solved or unsolved, and a hyperlink that takes you to the past versions of the problem.

thinkdev/problemlog/static/versions.html - The page that contains all past versions of the problem. 

thinkdev/problemlog/static/version-view.html - The page that shows the content of the previous problem version. The problem title, the version number of the problem, and the content.

thinkdev/problemlog/views.py - The views.py file contains all the Python functions that determine the behaviour of my webapp.

thinkdev/problemlog/urls.py - The urls.py file contains all the web paths of my webapp.

thinkdev/problemlog/models.py - The models.py file contains all the ORM models for my webapp. I used two models, a "Problems" model which contains all the problem entries, and a "ProblemVersions" model, which contains all the edited versions of the problem.

#### Business Logic Explanation:

The program works by saving entered content in text areas to a Django model called "Problems", keeping track of the user who created the problem. When a new problem is created, it first creates an entry in the "Problems" model, and then creates an entry in the "ProblemVersions" model, using the ID of the "Problems" model entry as a foreign key for the "ProblemVersions" model, linking all versions to the master problem. 

When navigated to, the "previously saved problems" page iterates through a variable that contains the results of a query of all unique problems created by the currently logged-in user, using Jinja for loops to display each problem in HTML. When the edit button is clicked next to a problem, the webapp redirects to a page that takes the "Problems" ID of the entry and passes it as a value into the "problem_log_edit" route. The "problem_log_edit" function in the views.py file uses the ID to query the "Problems" model, and fetch the correct content to then populate the relevant text areas with. After a problem is edited, the master problem is updated in the "Problems" model, and a new version is saved to the "ProblemVersions" model.

When the "Versions" hyperlink is clicked (next to a problem entry on the "previously saved problems" page), the webapp redirects to the "problem_versions" route, and again passes in the "Problems" ID of the problem to the route. This allows the "problem_versions" function in the views.py file to query all entries in the "ProblemVersions" model, with a matching problem_ID number. Jinja templating is then used to show each relevant entry in HTML. When the view button is clicked next to a version, the ID of the specific version is passed into the "versions_view" path, and a query is used to find and populate the "version-view.html" file with the correct content.

Finally, when a problem is deleted from the "previously saved problems" page, all versions of that problem in the "ProblemVersions" model are deleted via CASCADE.

#### Design Choices:

1. I first decided to only include one HTML template page, but I realised that having 2 templates would be far superior in reducing the repetition of code. So I introduced the layout.html template also.

2. I implemented some JavaScript to animate the home page text. The slogan "Because you should always think, before you dev." was animated to mimic a typewriter effect, with each letter showing up one at a time. It was too distracting however, so I decided to get rid of it. 

3. I originally had a delete button next to each version of the problem. I decided to remove this as it didn't make sense, and caused a few issues. For example, if I deleted the current problem version, it would cause all the other versions to be deleted as well.

4. Originally attempted to use HTML's table element to create the black sidebar and content for the main logged in pages, however switched to CSS-grid which was far more appropriate for the use case.

5. Text-area widths and heights were a lot bigger, and fixed. I changed this to make the text-areas automatically increase in height when a new line was entered (using the "field-sizing: content;" CSS property), allowing the user to always be able to see all of the entered content at once.
