import React from 'react';

class LoginPage extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            sessions: []
        }
        this.viewSessionPage = this.viewSessionPage.bind(this);
        this.newSession = this.newSession.bind(this);
        this.viewSession = this.viewSession.bind(this);
    }

    componentDidMount(){
        let urlForSessions = "/sessions";
        let self = this;
        fetch(urlForSessions,
        {
            method: 'GET'
        })
        .then((response)=>response.json())
        .then(function(session_list){
            self.setState({
                sessions: session_list['sessions']
            })
        })
        .catch((err)=>console.log(err));      
    }

    viewSessionPage(){
        let session_id = document.getElementById("session").value;
        this.props.viewBoard(session_id);
    }

    viewSession(session){
        this.props.viewBoard(session);
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
        .then((response)=>this.viewSession(response))
        .catch((err)=>console.log(err));
    }

    render(){
        let self = this;
        return(
            <div>
                <div class="title-bar">
                    <div class="title-div">
                        <h1 class="title">BwIC Web App</h1>                
                    </div>
                </div>
                <input type="text" id="session_name"></input>
                <button onClick={this.newSession}>New Session</button>
                <div>
                    {this.state.sessions.map(function(session){
                        return(<div>
                            <button onClick={()=>self.viewSession(session)}>{session.name}</button>
                        </div>);
                    })}
                </div>
            </div>
        );
    }
}

export default LoginPage;