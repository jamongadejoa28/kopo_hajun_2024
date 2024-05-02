const express = require('express');
const app = express();
const port = 80; // port number - ncp에서 열었던 포트 번호

app.get('/main', (req, res) => {
  res.sendfile('main.html');
});

app.get('/main2', (req, res) => {
  res.sendfile('main2.html');
});

app.get('/test', (req, res) => {
  res.sendfile('test.html');
});

app.get('/jq', (req, res) => {
  res.sendfile('jq.html');
});

app.get('/jq2', (req, res) => {
  res.sendfile('jq2.html');
});

app.get('/jq3', (req, res) => {
  res.sendfile('jq3.html');
});

app.get('/qsplus', function(req, res) {
    let num1 = Number(req.query.num1);
    let num2 = Number(req.query.num2);
    let num3 = Number(req.query.num3);
    let result = num1+num2+num3;
    res.send({result:result});
});

app.get('/buy', function(req,res){
  let num = Number(req.query.num);
  let item1 = Number(req.query.item1);
  let item2 = Number(req.query.item2);
  let item3 = Number(req.query.item3);
  let item4 = Number(req.query.item4);
  let item5 = Number(req.query.item5);
  let item6 = Number(req.query.item6);
  let item7 = Number(req.query.item7);

  if(num >= item7){
    res.send({message:`${item7}구입가능`});
  }
  else if(num >= item6){
    res.send({message:`${item6}구입가능`});
  }
  else if(num >= item5){
    res.send({message:`${item5}구입가능`});
  }
  else if(num >= item4){
    res.send({message:`${item4}구입가능`});
  }
  else if(num >= item3){
    res.send({message:`${item3}구입가능`});
  }
  else if(num >= item2){
    res.send({message:`${item2}구입가능`});
  }
  else if(num >= item1){
    res.send({message:`${item1}구입가능`});
  }
  else{
    res.send({message:"구입불가"});
  }
})

app.get('/buy2',function(req,res){
  let num = Number(req.query.num);
  let arr = [
    { name: "item1", price: 1000 },
    { name: "item2", price: 3000 },
    { name: "item3", price: 5000 },
    { name: "item4", price: 10000 },
    { name: "item5", price: 30000 },
    { name: "item6", price: 50000 },
    { name: "item7", price: 100000 },
    { name: "item8", price: 500000 }
  ];
  let max = 0;
  for (let i = 0; i < arr.length; i++) {
    if (arr[i].price <= num) {
      max = arr[i].price;
    } else {
      break;
    }
  }

  if (max >= arr[0].price) {
    res.send({ message: `${max}원 상품 구입 가능` });
  } else {
    res.send({ message: "구입 불가" });
  }

});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
