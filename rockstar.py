"""
rockstar.py contains main concepts and how-to's related to this project.

Main Concepts:
- What is Django?
- What is Selenium?
- What is geckodriver?


TDD Main Concepts:
- draw the process diagram for iterating between functional tests, unit tests, and code development.

How To:
- how to add a new column to a sql db?
- how to add a new url?
- difference between urls and
- how to auto-generate a new url? (/.+/ this is greedy and will match anything close to it)
"""

"""
When are trailing slashes important? 
What is the difference between ('/new/') and ('/new') ? 

Answer:
In TDD, he follows the convention where urls without trailing slashes are used to modify the db. Urls with a slash at 
the end do not require an action.
"""

"""
What do the status codes 404, 301, and 302 indicate?
404: not found
302: url has been redirected, i.e., temporarily moved
301: url has been permanently moved 

"""

"""
What is a ForeignKey? 


"""

"""
How do you pass data to a view function? 
self

How do you pass data to the render function?
response.context(['word'])  

What is the difference?
"""





