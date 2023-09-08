const fs = require('fs');

// Read the data from the "new_numbers.json" file
const rawData = fs.readFileSync('new_numbers.json', 'utf8');
const jsonData = JSON.parse(rawData);

// Convert timestamps to formatted date and time
const formattedData = jsonData.map(item => {
    const timestamp = item.timestamp;
    const date = new Date(timestamp);
    
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const seconds = date.getSeconds().toString().padStart(2, '0');
    
    const formattedTimestamp = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    
    return {
        number: item.number,
        formattedTimestamp: formattedTimestamp
    };
});

// Write the formatted data to the new file
fs.writeFileSync('new_datetime_numbers.json', JSON.stringify(formattedData, null, 2), 'utf8');

console.log('New file "new_datetime_numbers.json" created with converted date and time.');
