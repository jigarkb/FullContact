FullContact
===========

It includes a simple Python interface for FullContact API
Unlike from the library suggested on FullContact page this supports POST requests for Person Batch Requests. 
For time being I have only implemented Lookup by emails functionality for Batch Processing.

The Catch about the code is that you can have email list of more than 20 emails and my code will split it into 20 email chunk and process them separately and returns a combined easily readable and accessible one response.

Usage
===========
In the FullContact folder create your file and write:
For Batch Request

    from fullcontact import FullContact
    API_KEY='xxxx'
    fc=FullContact(API_KEY)
    email_list=["bart@fullcontact.com","you@email.com"]
    response=fc.post(email_list)

For Single Request

    from fullcontact import FullContact
    API_KEY='xxxx'
    fc=FullContact(API_KEY)
    person_profile=fc.get(email=<email_address>)
    
Response Data
===========
The data structure of response will be

For Batch Request

    {<email_address> : <Person Response Data>}

For Single Request

    {<Person Response Data>}
