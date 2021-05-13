const { spawn } = require('child_process');
const Best_Score = []; // Store readings

const sensor = spawn('python', ['Run.py']);
sensor.stdout.on('data', function(data) {

    // convert Buffer object to Float
    Best_Score.push(parseFloat(data));
    console.log(Best_Score);
});