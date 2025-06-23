# Health Insurance Claim Api 

### Description:
- This api is used for health insurance claims. It can generate,manage,delete claims by user. Built upon fastapi,this is a lightweight api which prioritizes security with JWT(JSON web tokens) and uses sqlite database for easy setup and running of database.

### Installation:
- To install all the dependencies and modules of this api,use:
    - **pip install -r requirements.txt** ,which is present in the root directory
- Use virtual environment for isolating all the dependencies and avoiding conflict with other modules

### Usage:
- To initialize this api, use the following code:
    - **uvicorn app.main:app --reload**
- This starts the api using app which is an instance to fastapi and we can then head to **localhost:8000** with the link provided in the terminal,thanks to uvicorn which is an ASGI server
- We can then head to SwaggerUi which contains automatic documentation with the path /docs and test the working off this api

### Workflow of this api:
- The user needs to sign-up first and the user is returned with a JWT authentication token which they can use to proceed further
    - This token has a time limit and after certain time ,this token will expire
    - This ensures security as token is no longer valid after certain amount of time
- The user then needs to sign-in with the aforementioned credentials.
    - If the credentials are not valid, the user is met with an error 401 (unauthorized access)
- The user can generate a claim which is handled by fastapi's POST operation
    - Here the users details are stored with index for easier retrieval and managing it
- After this step, the claim is stored in the database with one of three values
    - > PENDING
    - > APPROVED
    - > REJECTED
- The user can check this status with GET operation of fastapi()
- The claim status is then updated with PUT operation.
- This claim can be stored or deleted with DELETE operation.

![Education Whiteboard in Pastel Orange Teal Rose Pink Style](https://github.com/user-attachments/assets/7037070b-494a-42d5-9e21-7f0c4c3b5376)

- File Structure:

> app
- >core : Contains configuration,security aspect of api
- >models : Defines how the data is stored with SQLalchemy,enum... etc
- >Schemas: This validates what data user can send with pydantic syntax
- >routers : Defines the routing and endpoints of apis and also handles exception errors and rate limiting with slowapi
- >Tests : Used for testing the working of this api with pytest which runs automated tests

This api is structured by seperating all the different features of the api in different folders with each serving a different feature of api.
This structure provides various benefits such as:
    - Code maintainability
    - Easier management of code
    - Better scalability
- Instead of one giant block of code we are seperating each feature in a different and manageable files which also help in better readability of code
### How It All Fits Together:
- A user makes a request (e.g., GET /users/123).
- Routers receive the request and check security (core).
- Services fetch data from the database (models) or run background jobs.
- Schemas validate the data before sending it back.
- If something breaks, tests help catch the bug early.


##### Future improvements📰:
- Replacing Fastapi with flask for better versitality
- Using PostgreSQL or similar SQL DB's as SQLITE has its limitations
- Using Oauth2 instead of python-jose for better security
