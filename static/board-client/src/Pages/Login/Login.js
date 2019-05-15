import React from 'react';

class LoginPage extends React.Component{
    constructor(props){
        super(props);
        this.viewSessionPage = this.viewSessionPage.bind(this);
        this.newSession = this.newSession.bind(this);
        this.viewSession = this.viewSession.bind(this);
    }

    viewSessionPage(){
        let session_id = document.getElementById("session").value;
        this.props.viewBoard(session_id);
    }

    viewSession(session_id){
        this.props.viewBoard(session_id);
    }

    newSession(){
        let session_name = document.getElementById("session_name").value;
        let urlForBlockCommit = "/newsession";
        fetch(urlForBlockCommit,
        {
            method: 'POST',
            headers: {'Content-Type': 'text/plain'},
            body: JSON.stringify({'session_name':session_name})
        })
        .then((response)=>response.json())
        .then((response)=>this.viewSession(response['session_id']))
        .catch((err)=>console.log(err));
    }

    render(){
        return(
            <div>
                <input type="text" id="session"></input>
                <button onClick={this.viewSessionPage}>View Session</button>
                <input type="text" id="session_name"></input>
                <button onClick={this.newSession}>New Session</button>
            </div>
        );
    }
}

export default LoginPage;