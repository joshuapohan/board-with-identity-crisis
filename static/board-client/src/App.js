import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Board from './Pages/Board';
import Login from './Pages/Login';

class App extends Component {

    constructor(props){
        super(props);
        this.state = {
          mode: 0,
          session_id: 0
        };
        this.viewBoard = this.viewBoard.bind(this);
    }

    viewBoard(session_id){
        this.setState(
            {
              mode:1,
              session_id: session_id
            }
        );
    }

    render() {
        let self = this;
        return (
            <div className="App">
                {   
                    function(){
                        switch(self.state.mode){
                            case 0:
                                return  <Login viewBoard={self.viewBoard}/>;
                            case 1:
                                return <Board session_id={self.state.session_id}/>;
                            default:
                                return <Login viewBoard={self.viewBoard}/>;
                        }
                    }()
                }
            </div>
        );
    }
}

export default App;