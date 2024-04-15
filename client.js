const net = require('net');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const client = new net.Socket();
const socketPath = '/tmp/socket_file';

const functionMap = {
    'floorArea': { argCount: 1, argTypes: ['number'] },
    'nrootArea': { argCount: 2, argTypes: ['number', 'number'] },
    'reverseArea': { argCount: 1, argTypes: ['string'] },
    'validAnagramArea': { argCount: 2, argTypes: ['string', 'string'] },
    'sortArea': { argCount: 1, argTypes: ['array'] } // 配列を1つの引数として扱う
};

client.connect(socketPath, () => {
    console.log('サーバーに接続しました。');
    selectFunction();
});

function selectFunction() {
    console.log('使用する関数を以下から選択してください:');
    Object.keys(functionMap).forEach((func, index) => {
        console.log(`${index + 1}: ${func}`);
    });
    
    rl.question('関数番号を入力してください: ', (number) => {
        const functionNames = Object.keys(functionMap);
        const functionName = functionNames[number - 1];
        
        if (functionName) {
            requestArguments(functionName);
        } else {
            console.log('無効な番号です。');
            selectFunction();
        }
    });
}

function requestArguments(functionName) {
    const numArgs = functionMap[functionName].argCount;
    const args = [];
    const argTypes = functionMap[functionName].argTypes;

    console.log(`${functionName}関数は${numArgs}個の引数が必要です。`);
    
    const getArg = (index) => {
        if (index < numArgs) {
            rl.question(`引数${index + 1}を入力してください (${argTypes[index]}): `, (arg) => {
                args.push(argTypes[index] === 'number' ? parseFloat(arg) : arg);
                getArg(index + 1);
            });
        } else {
            sendRequest(functionName, args);
        }
    };

    getArg(0);
}

function sendRequest(functionName, args) {
    const dataToSend = {
        method: functionName,
        params: args,
        param_types: functionMap[functionName].argTypes,
        id: 1
    };
    
    client.write(JSON.stringify(dataToSend));
    rl.close();
}

client.on('data', (data) => {
    console.log('サーバーからの応答:', data.toString());
    client.end();
});

client.on('close', () => {
    console.log('サーバーとの接続が切断されました。');
});
