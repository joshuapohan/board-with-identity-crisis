import React from 'react';
import './Login.css';

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
                <div className="title-bar">
                    <div className="title-div">
                        <h1 className="title">BwIC Web App</h1>                
                    </div>
                </div>
                <div className="main-content">
                    <input type="text" id="session_name"></input>
                    <button onClick={this.newSession}>New Session</button>
                    <div className="session-div-container">
                        <div className="session-div">
                            <h2 className="session-title">Sessions : </h2>
                            <table>
                                {this.state.sessions.map(function(session){
                                    return(
                                        <React.Fragment>
                                            <tr>
                                                <td className="session-title">{session.name}</td>
                                                <td><button className="main-button" onClick={()=>self.viewSession(session)}>View</button></td>
                                            </tr>
                                        </React.Fragment>
                                    );
                                })}
                            </table>
                        </div>
                    </div> 
                </div>
            </div>
        );
    }
}

export default LoginPage;