var express = require('express');
var router = express.Router();
var Querie = require('../controllers/querie')
var py = require('python-shell');

/* GET home page. */
router.get('/', (req, res) => {
  res.render('index')
})

router.get('/python',async (req,res) =>{
    await py.PythonShell.run('C:/Users/joaop/Desktop/AEBD(API Rest) - Local/script.py', null,(erro) => {
            if (erro) console.log('Error: Run Script ' + JSON.stringify(erro))
            else{
              console.log('Script run successfully')
            }
    })

    res.render('index')

})

router.get('/users',(req,res) =>{
  var n = 'Users'
  Querie.getUsers()
       .then(dados => {
            res.render('tUsers',{nome:n,tabela:dados})
       })
       .catch(erro => {
            res.render('index')
            console.log("Error: " + erro)
        })
})


router.get('/users/history',(req,res)=>{
  var n = 'Users History'
  Querie.getUsersHistory()
      .then(dados => {
          res.render('tUsers',{nome:n,tabela:dados})
      })
      .catch(erro => {
          res.render('index')
          console.log("Error: " + erro)
      })
})

router.get('/tablespaces',(req,res)=>{
  var n = 'Tablespaces'
  Querie.getTablespaces()
        .then(dados => {
            res.render('tTablespaces',{nome:n,tabela:dados})
        })
        .catch(erro => {
            res.render('index')
            console.log("Error: " + erro)
        })
})

router.get('/tablespaces/history',(req,res)=>{
  var n = 'Tablespaces History'
  Querie.getTablespacesHistory()
        .then(dados => {
            res.render('tTablespacesHistory',{nome:n,tabela:dados})
        })
        .catch(erro => {
            res.render('index')
            console.log("Error: " + erro)
        })
})

router.get('/datafiles',(req,res)=>{
  var n = 'Datafiles'
  Querie.getDatafiles()
        .then(dados => {
            res.render('tDatafiles',{nome:n,tabela:dados})
        })
        .catch(erro => {
            res.render('index')
            console.log("Error: " + erro)
        })
})

router.get('/datafiles/history',(req,res)=>{
  var n = 'Datafiles History'
  Querie.getDatafilesHistory()
        .then(dados => {
              res.render('tDatafilesHistory',{nome:n,tabela:dados})
        })
        .catch(erro => {
              res.render('index')
              console.log("Error: " + erro)
        })
})

router.get('/sessions',(req,res)=>{
  var n = 'Sessions'
  Querie.getSessions()
        .then(dados => {
            res.render('tSessions',{nome:n,tabela:dados})
        })
        .catch(erro => {
            res.render('index')
            console.log("Error: " + erro)
        })
})

router.get('/sessions/history',(req,res)=>{
  var n = 'Sessions History'
  Querie.getSessionsHistory()
        .then(dados => {
              res.render('tSessionsHistory',{nome:n,tabela:dados})
        })
        .catch(erro => {
            res.render('index')
            console.log("Error: " + erro)
        })
})

router.get('/memory',(req,res)=>{
  var n = 'Memory'
  Querie.getMemory()
        .then(dados => {
              res.render('tMemory',{nome:n,tabela:dados})
        })
        .catch(erro => {
              res.render('index')
              console.log("Error: " + erro)
        })
})

router.get('/memory/history',(req,res)=>{
  var n = 'Memory History'
  Querie.getMemoryHistory()
        .then(dados => {
              res.render('tMemoryHistory',{nome:n,tabela:dados})
        })
        .catch(erro => {
              res.render('index')
              console.log("Error: " + erro)
        })
})

router.get('/roles',(req,res)=>{
  var n = 'Roles'
  Querie.getRoles()
       .then(dados => res.render('tRoles',{nome:n,tabela:dados}))
       .catch(erro => {
            res.render('index')
            console.log("Error: " + erro)
        })
})

router.get('/memory/cdb',(req,res)=>{
      var n = 'Memory by PGA'
      Querie.getMemCDB()
           .then(dados => res.render('tMemoryCDB',{nome:n,tabela:dados}))
           .catch(erro => {
                res.render('index')
                console.log("Error: " + erro)
            })
})

router.get('/memory/dba',(req,res)=>{
      var n = 'Memory PGA and SGA'
      Querie.getMemDBA()
           .then(dados => res.render('tMemoryDBA',{nome:n,tabela:dados}))
           .catch(erro => {
                res.render('index')
                console.log("Error: " + erro)
            })
})

router.get('/memory/dataStorage',(req,res)=>{
      var n = 'Data Storage Memory '
      Querie.getMemDataStorage()
           .then(dados => res.render('tMemoryDataStorage',{nome:n,tabela:dados}))
           .catch(erro => {
                res.render('index')
                console.log("Error: " + erro)
            })
})
    
    



router.get('/views',(req,res) =>{
    res.render('views')
})

router.get('/views/tab',(req,res) =>{
    var n = 'Tablespaces with Datafiles'
    Querie.getTabDatafiles()
          .then(dados => res.render('tabdatafiles',{nome:n,tabela:dados}))
          .catch(erro => {
                res.render('index')
                console.log("Error: " + erro)
        })
})

router.get('/views/user/hist',(req,res)=>{
    var n = 'User history by timestamp'
    Querie.getUserHist()
          .then(dados => res.render('userHist',{nome:n,tabela:dados}))
          .catch(erro => {
                res.render('index')
                console.log("Error: " + erro)
        })
})

router.get('/views/tab/hist',(req,res)=>{
    var n = 'Tablespace history by timestamp'
    Querie.getTablespaceHist()
          .then(dados => res.render('tablespaceHist',{nome:n,tabela:dados}))
          .catch(erro => {
                res.render('index')
                console.log("Error: " + erro)
        })
})

router.get('/views/dat/hist',(req,res)=>{
    var n = 'Datafile history by timestamp'
    Querie.getDataFileHist()
          .then(dados => res.render('datafilehist',{nome:n,tabela:dados}))
          .catch(erro => {
                res.render('index')
                console.log("Error: " + erro)
        })  
})

router.get('/views/ses/hist',(req,res)=>{
    var n = 'Sessions history by timestamp'
    Querie.getSessionsHist()
          .then(dados => res.render('sessionsHist',{nome:n,tabela:dados}))
          .catch(erro => {
                res.render('index')
                console.log("Error: " + erro)
        })    
})

router.get('/views/mem/hist',(req,res)=>{
    var n = 'Memory history by timestamp'
    Querie.getMemHist()
          .then(dados => res.render('memHist',{nome:n,tabela:dados}))
          .catch(erro => {
                res.render('index')
                console.log("Error: " + erro)
        })    
})

router.get('/views/user/rolesTab',(req,res)=>{
    var n = 'User with Roles and Tablespaces'
    Querie.getUserRolesTablespaces()
          .then(dados => res.render('userRolesTablespaces',{nome:n,tabela:dados}))
          .catch(erro => {
                res.render('index')
                console.log("Error: " + erro)
        }) 
})

router.get('/views/user/status',(req,res)=>{
    var n = 'User Status Open'
    Querie.getUserOpenStatus()
          .then(dados => res.render('userOpenStatus',{nome:n,tabela:dados}))
          .catch(erro => {
                res.render('index')
                console.log("Error: " + erro)
        }) 
})

router.get('/views/mem/histcbd',(req,res)=>{
      var n = 'Memory History by PGA'
      Querie.getMemHistCDB()
            .then(dados => res.render('memhistCDB',{nome:n,tabela:dados}))
            .catch(erro => {
                  res.render('index')
                  console.log("Error: " + erro)
          }) 
})

router.get('/views/mem/histdba',(req,res)=>{
      var n = 'Memory History by SGA'
      Querie.getMemHistDBA()
            .then(dados => res.render('memhistDBA',{nome:n,tabela:dados}))
            .catch(erro => {
                  res.render('index')
                  console.log("Error: " + erro)
          }) 
})

router.get('/views/mem/histdataStorage',(req,res)=>{
      var n = 'Memory History by Data Storage'
      Querie.getMemHistDataStorage()
            .then(dados => res.render('memhistDataStorage',{nome:n,tabela:dados}))
            .catch(erro => {
                  res.render('index')
                  console.log("Error: " + erro)
          }) 
})





module.exports = router;
