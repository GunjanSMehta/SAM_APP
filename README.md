aws-sam-guide

AWS SAM
The AWS Serverless Application Model (AWS SAM) is a open-source framework created to define, build, run and test serverless applications on AWS.
SAM consists of 2 main components:


SAM Template: contains the definiton of resources which are part of your application, using a simple and clean syntax

SAM Command line interface (CLI): tool to build, deploy and test serverless applications that are defined by SAM templates

All the resources supported by CloudFormation are also supported by SAM. In addiction, SAM provides you with extra resources which make them easier to work with and that are listed below:


AWS::Serverless::Function: Lambda Function

AWS::Serverless::Api: REST API Gateway

AWS::Serverless::HttpApi: HTTP API Gateway

AWS::Serverless::LayerVersion: Lambda Function Layer

AWS::Serverless::SimpleTable: DynamoDB table with a single attribute primary key

AWS::Serverless::Application: Serverless application from the AWS Serverless Application Repository or Amazon S3

This guide covers examples with AWS::Serverless::Function and AWS::Serverless::HttpApi resources.

How to install
if you run Python 2.7 on your machine, execute:
pip install aws-sam-cli
or Python >= 3.6:
pip3 install aws-sam-cli
Otherwise refer to the AWS documentation:
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html

Tutorial
This tutorial helps you to deploy your first SAM application on the mantel group sandpit1 account.
If you still don't have your bash profile configured to acquire the sandpit credentials through okta, execute the steps described in the following link:
https://gitlab.mantelgroup.com.au/cmd/onboarding/-/blob/master/authenticating-to-aws.md

Requirements
For local testing, SAM provide a Docker container similar to an execution environment hosting AWS Lambda. Hence, in addiction to the SAM CLI, it is required a docker installation.

Create your application
The folder sam-app contains the files required to run your first sam application that consist of a simple Lambda function.
Change the current working directory:
cd sam-app
The template template.yaml defines a simple lambda function, whose code is hosted in the hello_world folder.

Build
Execute the following exports to ensure you are pointing to the proper account:
export AWS_DEFAULT_REGION=ap-southeast-2
export AWS_DEFAULT_PROFILE=idp-sandpit1
In order to locally test or deploy the application on AWS you need to build the app:
sam build --use-container
This command must be executed every time you update your files (template, lambda, ..)

Deploy
Once the build finish, deploy your application on AWS:
sam deploy --guided
The first time you run the deploy, you will be asked to insert few parameters:


Stack Name: sam-app

AWS Region: au-southeast-2

Parameter Prefix: {your name}

Confirm changes before deploy [y/N]: y

Allow SAM CLI IAM role creation [Y/n]: y

Save arguments to samconfig.toml [Y/n]: y

SAM store these parameters in samconfig.toml, so the subsequent deploy command will not need the --guided option.
You can also run locally your lambda for test and debug purpose, even before deploying on AWS:
sam local invoke "HelloWorldFunction" -e event.json

Integrate an Http API gateway
Exploiting the potential of sam,  we can easily define a HTTP API Gateway resource as a lambda source.
Open your template.yaml and add the following Events resource to the properties of the HelloWorldFunction resource
  Events:
    HelloWorld:
      Type: HttpApi
      Properties:
        Path: /hello
        Method: get
Note that the same code in CloudFormation would have taken more than 20 lines.
In the Output section of your template, add the below resource which will display the API gateway endpoint URL for our Lambda
HelloWorldApi:
  Description: "API Gateway endpoint URL for Hello World function"
  Value: !Sub "https://${ServerlessHttpApi}.execute-api.${AWS::Region}.amazonaws.com/hello"
Build and Deploy your updated application:
sam build --use-container
sam deploy
Once the deployment finish, SAM will display your API gateway endpoint URL.
Test your API:
curl {HelloWorldApi output value}
Find out more about other implicit resources you can reference within SAM:
https://github.com/awslabs/serverless-application-model/blob/master/docs/internals/generated_resources.rst

Cloudformation extension
Being sam an extension of CloudFormation, it is capable of deploying all the resources supported by CF.
In this example, we are going to include a Bucket resource in our sam application.
Add the following snippet in the Resources list in your template:
Type: AWS::S3::Bucket
Properties:
  BucketName: cmdlab-sam-test-{your name}
Build and Deploy your updated application:
sam build --use-container
sam deploy
Test if the bucket has been effectively created:
aws s3 ls

Delstroy your sam application
SAM does not support the deletion of the application, so it must be done using the aws cli and destroying the application stack:
aws cloudformation delete-stack --stack-name sam-app
