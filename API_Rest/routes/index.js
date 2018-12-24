var express = require('express');
var router = express.Router();
var oracledb = require('oracledb')


/* GET home page. */
router.get('/', (req, res) => {
  res.render('index')
})

router.get('/users',(req,res) =>{
  var n = 'Users'
  res.render('index',{nome: n})
})


router.get('/users/history',(req,res)=>{
  var n = 'Users History'
  res.render('index',{nome: n})
})

router.get('/tablespaces',(req,res)=>{
  var n = 'Tablespaces'
  res.render('index',{nome: n})
})

router.get('/tablespaces/history',(req,res)=>{
  var n = 'Tablespaces History'
  res.render('index',{nome: n})
})

router.get('/datafiles',(req,res)=>{
  var n = 'Datafiles'
  res.render('index',{nome: n})
})

router.get('/datafiles/history',(req,res)=>{
  var n = 'Datafiles History'
  res.render('index',{nome: n})
})

router.get('/sessions',(req,res)=>{
  var n = 'Sessions'
  res.render('index',{nome: n})
})

router.get('/sessions/history',(req,res)=>{
  var n = 'Sessions History'
  res.render('index',{nome: n})
})

router.get('/memory',(req,res)=>{
  var n = 'Memory'
  res.render('index',{nome: n})
})

router.get('/memory/history',(req,res)=>{
  var n = 'Memory History'
  res.render('index',{nome: n})
})

router.get('/roles',(req,res)=>{
  var n = 'Roles'
  res.render('index',{nome: n})
})

module.exports = router;
