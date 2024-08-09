// import PocketBase from 'pocketbase';
const { PocketBase } = require('pocketbase');
(async function() {
const pb = new PocketBase('http://127.0.0.1:8090');


// fetch a paginated records list
const resultList = await pb.collection('spotify').getList(1, 50, {
    filter: 'created >= "2022-01-01 00:00:00" && someFiled1 != someField2',
});

// you can also fetch all records at once via getFullList
const records = await pb.collection('spotify').getFullList(200 /* batch size */, {
    sort: '-created',
});

// or fetch only the first record that matches the specified filter
const record = await pb.collection('spotify').getFirstListItem('someField="test"', {
    expand: 'relField1,relField2.subRelField',
});
})()