# Task Tracker API - Serverless Backend

This project demonstrates how to build a simple, serverless task tracker backend using AWS services. **The objective of this project is to learn how to utilize the AWS Cloud Development Kit (CDK) to address a straightforward project designed for educational purposes.** The API allows users to create, retrieve, update, and delete tasks, and is powered by AWS Lambda, API Gateway, and DynamoDB. This backend is designed to be cost-effective, scalable, and easy to maintain, providing a solid foundation for learning AWS CDK in TypeScript.

## Features

- **Create Task:** Add a new task with a title, description, and status.
- **Get Tasks:** Retrieve all tasks or a specific task by ID.
- **Update Task:** Modify an existing task's details.
- **Delete Task:** Remove a task by ID.

## Architecture

### AWS Services Used

- **AWS Lambda:** Five Lambda functions to handle CRUD operations (`CreateTask`, `GetTasks`, `GetTaskById`, `UpdateTask`, and `DeleteTask`).
- **AWS API Gateway:** Exposes REST API endpoints to interact with the Lambda functions.
- **AWS DynamoDB:** Stores task data in a pay-as-you-go model with on-demand pricing, ensuring cost efficiency.
- **AWS CloudWatch Logs:** Logs Lambda executions for monitoring and debugging.

## Benefits

- **Serverless:** The architecture scales automatically based on demand, with minimal setup and maintenance.
- **Cost-effective:** DynamoDB's on-demand pricing ensures you only pay for the data you store and the requests you make.
- **Hands-on CDK Learning:** This project provides an opportunity to practice using the AWS CDK with TypeScript, covering key concepts such as stacks, constructs, permissions, and deployment.

## How to Use

1. Clone the repository.
2. Set up AWS credentials with the required permissions.
3. Use AWS CDK to deploy the infrastructure and Lambda functions.
4. Test the API using tools like Postman or curl.

## Technologies Used

- AWS CDK (TypeScript)
- AWS Lambda
- API Gateway
- DynamoDB
- CloudWatch Logs

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
