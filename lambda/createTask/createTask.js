const AWS = require( 'aws-sdk' );
const docClient = new AWS.DynamoDB.DocumentClient();

exports.handler = async ( event ) => {
    const body = JSON.parse( event.body );
    const task = {
        taskId: body.taskId,
        title: body.title,
        description: body.description,
        status: body.status,
    };

    await docClient
        .put( {
            TableName: process.env.TABLE_NAME,
            Item: task,
        } )
        .promise();

    return {
        statusCode: 201,
        body: JSON.stringify( { message: 'Task created successfully!', task } ),
    };
};