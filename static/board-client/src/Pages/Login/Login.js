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
        let self = this;
        return(
            <div>
                <input type="text" id="session"></input>
                <button onClick={this.viewSessionPage}>View Session</button>
                <input type="text" id="session_name"></input>
                <button onClick={this.newSession}>New Session</button>
                <div>
                    {this.state.sessions.map(function(session){
                        return(<div>
                            <button onClick={()=>self.viewSession(session._id)}>{session.name}</button>
                        </div>);
                    })}
                </div>
            </div>
        );
    }
}

export default LoginPage;