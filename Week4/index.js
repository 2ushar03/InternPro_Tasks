const express=require('express')
const rateLimit=require('express-rate-limit');

const app=express();
const port=5000;

const setLimit=rateLimit({
    windowMs:10*60*1000,
    max:50,
    message:"Too many requests. Please try again in 15 minutes.",
})

app.use(setLimit);

app.get('/',(req,resp)=>{
    resp.send("API Call Successful!");
})

app.listen(port,()=>{
    console.log("Serever is running at Port",port);
})

