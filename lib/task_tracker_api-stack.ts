import * as apigatewayv2 from 'aws-cdk-lib/aws-apigatewayv2';
import * as integrations from 'aws-cdk-lib/aws-apigatewayv2-integrations';
import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import * as path from 'path';

export class TaskTrackerApiStack extends cdk.Stack {
  constructor (scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB Table
    const table = new dynamodb.Table(this, 'TasksTable', {
      partitionKey: { name: 'taskId', type: dynamodb.AttributeType.STRING },
      tableName: 'Tasks',
      removalPolicy: cdk.RemovalPolicy.DESTROY, // Allows us to delete the table when the stack is deleted
    });

    // Lambda Functions
    const createTaskFunction = new lambda.Function(this, 'CreateTaskFunction', {
      runtime: lambda.Runtime.NODEJS_22_X,
      code: lambda.Code.fromAsset('lambda/createTask'),
      handler: 'createTask.handler',
      environment: {
        TABLE_NAME: table.tableName,
      },
    });

    const listTasksFunction = new lambda.Function(this, 'ListTasksFunction', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'list_tasks.lambda_handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/listTasksPython')),
      environment: {
        TABLE_NAME: table.tableName, // Ensure `table` is your DynamoDB table reference
      },
    });

    // Add Delete Task Lambda
    const deleteTaskFunction = new lambda.Function(this, 'DeleteTaskFunction', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'delete_task.lambda_handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/deleteTask')),
      environment: {
        TABLE_NAME: table.tableName,
      },
    });

    // Grant DynamoDB Permissions
    table.grantReadWriteData(createTaskFunction);
    table.grantReadData(listTasksFunction);
    table.grantWriteData(deleteTaskFunction);

    // API Gateway
    // Create HTTP API Gateway
    const httpApi = new apigatewayv2.HttpApi(this, 'TaskTrackerHttpApi', {
      apiName: 'TaskTrackerHttpApi',
      corsPreflight: {
        allowHeaders: ['Content-Type'],
        allowMethods: [apigatewayv2.CorsHttpMethod.GET, apigatewayv2.CorsHttpMethod.POST, apigatewayv2.CorsHttpMethod.DELETE],
        allowOrigins: ['*'],
      }
    });

    // Add a route for the HTTP GET method to the /tasks endpoint
    httpApi.addRoutes({
      path: '/tasks',
      methods: [ apigatewayv2.HttpMethod.GET ],
      integration: new integrations.HttpLambdaIntegration('ListTasksIntegration', listTasksFunction),
    });

    // Add a route for the HTTP POST method to the /tasks endpoint
    httpApi.addRoutes({
      path: '/tasks',
      methods: [ apigatewayv2.HttpMethod.POST ],
      integration: new integrations.HttpLambdaIntegration('CreateTaskIntegration', createTaskFunction),
    });

    // Add DELETE route
    httpApi.addRoutes({
      path: '/tasks/{taskId}',
      methods: [ apigatewayv2.HttpMethod.DELETE ],
      integration: new integrations.HttpLambdaIntegration('DeleteTaskIntegration', deleteTaskFunction),
    });

    // Output the HTTP API endpoint
    new cdk.CfnOutput(this, 'HttpApiEndpoint', {
      value: httpApi.apiEndpoint,
    });
  }
}