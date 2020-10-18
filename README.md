# Piazza Bot for Slack
### Overview
___
This was a project created for the UVA GWC Hackathon 2020. The goal of this project was to help students and faculty in the current online ecosystem. We did so by creating a Slack Bot that would help students answer basic questions such as `Show me the last 3 piazza posts` or `Can I view the previous 4 answered piazza posts`. The idea was to allow students to remain in one econsystem (Slack) and still easily access their data from multiple platforms.

### Architecture

___

Slack Bot was designed to interface with API Gateway which would then send the data to a Lambda function.

### Usage

___

To set up, create a Slack Bot that acts on events when the bot is mentioned. Then, created a REST API Gateway as well as a Lambda function. Within the Lambda function, upload the file function.zip. There are four key environment variables that also must be accounted for.


| Env Var        | Value           | 
| ------------- |:-------------:|
| piazza_email      | email@email.com |
| piazza_password      | *******      | 
| slack_token | Found on Slack API Website      |
|classID|Found on Piazza|


Once these variables are inputted, you can begin usage of the Slack Bot.

### Updating

___

To update `function.zip` use the following shell command `zip -g function.zip myfile.py`. Similarly, to add additional functionality using another library use `pip install --target ./package packageName`
