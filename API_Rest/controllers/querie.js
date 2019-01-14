var oracledb = require('oracledb')

const Querie = module.exports

Querie.getUsers = async() =>{
    var query = 'SELECT * FROM USER_T'
    var result = await ex(query)
    return result
}

Querie.getUsersHistory = async() =>{
    var query = 'SELECT * FROM USER_HISTORY'
    var result = await ex(query)
    return result
}

Querie.getTablespaces = async() =>{
    var query = 'SELECT * FROM TABLESPACE_T'
    var result = await ex(query)
    return result
}

Querie.getTablespacesHistory = async() =>{
    var query = 'SELECT * FROM TABLESPACE_HISTORY'
    var result = await ex(query)
    return result
}

Querie.getDatafiles = async() =>{
    var query = 'SELECT * FROM DATAFILE_T'
    var result = await ex(query)
    return result
}

Querie.getDatafilesHistory = async() =>{
    var query = 'SELECT * FROM DATAFILE_HISTORY'
    var result = await ex(query)
    return result
}

Querie.getSessions = async() =>{
    var query = 'SELECT * FROM SESSIONS'
    var result = await ex(query)
    return result
}

Querie.getSessionsHistory = async() =>{
    var query = 'SELECT * FROM SESSIONS_HISTORY'
    var result = await ex(query)
    return result
}

Querie.getMemory = async() =>{
    var query = 'SELECT * FROM MEMORY_T'
    var result = await ex(query)
    return result
}

Querie.getMemoryHistory = async() =>{
    var query = 'SELECT * FROM MEMORY_HISTORY'
    var result = await ex(query)
    return result
}

Querie.getRoles = async() =>{
    var query = 'SELECT * FROM ROLE_T'
    var result = await ex(query)
    return result
}

Querie.getTabDatafiles = async() =>{
    var query = 'SELECT * FROM tab_dataFiles'
    var result = await ex(query)
    return result
}

Querie.getMemHist = async() =>{
    var query = 'SELECT * FROM mem_hist'
    var result = await ex(query)
    return result
}

Querie.getDataFileHist = async() =>{
    var query = 'SELECT * FROM datafile_hist'
    var result = await ex(query)
    return result
}

Querie.getSessionsHist = async() =>{
    var query = 'SELECT * FROM sessions_hist'
    var result = await ex(query)
    return result
}

Querie.getTablespaceHist = async() =>{
    var query = 'SELECT * FROM tablespace_hist'
    var result = await ex(query)
    return result
}

Querie.getUserHist = async() =>{
    var query = 'SELECT * FROM user_hist'
    var result = await ex(query)
    return result
}

Querie.getUserOpenStatus = async() =>{
    var query = 'SELECT * FROM user_openStatus'
    var result = await ex(query)
    return result
}

Querie.getUserRolesTablespaces = async() =>{
    var query = 'SELECT * FROM  user_roles_tablespaces'
    var result = await ex(query)
    return result
}


const ex = (query) => {
    return new Promise((resove, reject) => {
            oracledb.getConnection(
                {
                    user: 'jjnm',
                    password: 'oracle',
                    connectString: '127.0.0.1/orcl' 
                },(erro,connect)  =>{
                    if(!erro){
                        connect.execute(query,{},{outFormat: oracledb.OBJECT},(err,result)=>{
                            if(!err){
                                resove(result.rows)
                            }
                            else{
                                reject(err)
                                console.log('Error: Query ' + JSON.stringify(err))
                            }
                        })
                    }
                    else{
                        console.log('Error: Connection ' + JSON.stringify(erro))
                    }
                })
    })
  }

