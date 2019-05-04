import React from 'react';

class LoginPage extends React.Component{
    constructor(props){
        super(props);
        this.viewSessionPage = this.viewSessionPage.bind(this);
    }

    viewSessionPage(){
        let session_id = document.getElementById("session").value;
        this.props.viewBoard(session_id);
    }

    render(){
        return(
            <div>
                <input type="text" id="session"></input>
                <button onClick={this.viewSessionPage}>View Session</button>
            </div>
        );
    }
}

export default LoginPage;