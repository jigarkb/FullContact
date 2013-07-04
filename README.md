FullContact
===========

It includes Python Library for FullContact API
Unlike from the library suggested on FullContact page this supports POST requests for Person Batch Requests. 

Usage
===========
In the FullContact folder create your file and write:

    from fullcontact import FullContact
    API_KEY='xxxx'
    fc=FullContact(API_KEY)
    email_list=["bart@fullcontact.com","you@email.com"]
    response=fc.post(email_list)

Response Data
===========
The data structure of response will be

    {<email from email_list> : <Person Response Data>}
