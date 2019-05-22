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
          session: null
        };
        this.viewBoard = this.viewBoard.bind(this);
        this.viewMain = this.viewMain.bind(this);
    }

    viewBoard(session){
        this.setState(
            {
              mode:1,
              session: session
            }
        );
    }

    viewMain(){
        this.setState(
            {
                mode:0,
                session:null
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
                                return <Board session={self.state.session} viewMain={self.viewMain}/>;
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