const AWS = require( 'aws-sdk' );
const docClient = new AWS.DynamoDB.DocumentClient();

exports.handler = async ( event ) => {
    console.log( 'Event received:', JSON.stringify( event, null, 2 ) );

    try {
        const body = JSON.parse( event.body );
        console.log( 'Parsed body:', body );

        const task = {
            taskId: body.taskId,
            title: body.title,
            description: body.description,
            status: body.status,
        };
        console.log( 'Task to be created:', task );

        await docClient.put( {
            TableName: process.env.TABLE_NAME,
            Item: task,
        } ).promise();
        console.log( 'Task successfully written to DynamoDB' );

        return {
            statusCode: 201,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify( {
                message: 'Task created successfully!',
                task
            } )
        };
    } catch ( error ) {
        console.error( 'Error occurred:', error );
        return {
            statusCode: 500,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify( {
                message: 'Failed to create task',
                error: error.message,
                stackTrace: error.stack
            } )
        };
    }
};