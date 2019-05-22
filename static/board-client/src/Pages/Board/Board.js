import React from 'react';
import './Board.css';
import showdown from 'showdown';

const TasksBlockDivStyle = {
  backgroundColor: 'white',
  width: '300px',
  minHeight: '300px',
  display: 'inline-block',
  marginRight: '30px',
  textAlign: 'center',
  verticalAlign: 'top',
  marginTop: '10px',
  fontFamily: 'Roboto'
}

const TaskViewStyle = {
  width: '250px',
  minHeight: '50px',
  borderRadius: '18px',
  display: 'block',
  margin: 'auto',
  marginTop: '5px',
  marginBottom: '5px',
  fontFamily: 'Roboto',
  textAlign: 'center',
  wordWrap: 'break-word',
  transition: '0.2s'
}

const TextInputStyle = {
  outline: 'none',
  backgroundColor: 'inherit',
  border: 'none',
  width: '100%',
  minWidth: '100%',
  maxWidth: '100%',
  minHeight: '100px',
  fontFamily: 'Roboto'
}

const TitleInputStyle = {
  outline: 'none',
  backgroundColor: 'inherit',
  marginTop: '10px',
  border: 'none',
  width: '100%',
  minWidth: '100%',
  maxWidth: '100%',
  fontFamily: 'Roboto'        
}

const TitleStyle = {
  margin: '0px'
}

const TextContainerStyle = {
  padding: '10px',
}

const DeleteButtonStyle ={
  textAlign: 'right'
}

const SessionHeadingStyle = {
  textAlign: 'center',
  color: 'white',
  fontFamily: 'Roboto',
  backgroundColor: 'black',
  padding: '5px'
}

class TasksBlock extends React.Component{
    constructor(props){
        super(props)
          /* debugging purposes */
          let tasks = [];
          if(this.props.instanceObj){
              //debug
              this.props.instanceObj.myTasks.forEach((task)=>{
                  tasks.push({
                    _id: 'task' + task._id, 
                    _title:task._name, 
                    _text:task.detail,
                    color_id: task.color_id, 
                    owner_id: this.props._id
                  });
              });
          }
          /* end debug */
        /* mode 0 for view mode, 1 for edit mode*/
        this.state = {
          mode: 0,
          _id: this.props._id || this.props.instanceObj._id || -999,
          _title: this.props._name || this.props.instanceObj._name || 'Box',
          myTasks: tasks,
          session_id: this.props.session_id || 0
        };
      
        this.taskInstances = [];
        this.allowDrop = this.allowDrop.bind(this);
        this.drop = this.drop.bind(this);
        this.printTasks = this.printTasks.bind(this);
        this.addTaskRef = this.addTaskRef.bind(this);
        this.saveBlock = this.saveBlock.bind(this);
        this.switchMode = this.switchMode.bind(this);
        this.saveToServer = this.saveToServer.bind(this);
    }
    addTaskRef(instance){
        this.taskInstances = this.taskInstances.concat([instance]);
    }
    printTasks(){
        this.taskInstances.forEach((curTask)=>{
            console.log(curTask);
        });
    }
    allowDrop(ev){
        ev.preventDefault();
    }
    drop(ev){
        ev.preventDefault();
        let taskObj = JSON.parse(ev.dataTransfer.getData("taskObj"));
        /* Remove task from the previous owner / block first, previous block state will be updated and rerendered*/
        this.props.removeTask(taskObj._id, taskObj.owner_id);
        taskObj.owner_id = this.state._id;
        /* Append the task object and rerender current block 
           Pros : tasks are handled through react instances instead of moving around the DOM element
           Cons : all the related blocks and tasks are re rendered, might take long
        */
        this.setState({
            myTasks: this.state.myTasks.concat([taskObj])
        }, this.saveToServer);
        
        
    }
    switchMode(ev){
        /* mode 1 is for modification mode */
        this.setState({
            mode:1
        });
    }
    saveBlock(ev){
        /** Executed on button click in task edit mode , mode 0 for view mode*/
        let newTitle = document.getElementById('input' + this.state._id).value;
        this.setState({
            mode: 0,
            _title: newTitle
        }, this.saveToServer);
    }
    saveToServer(){
        /**
            function to send update to server using task id and container id
        */
        let urlForBlockCommit = "https://bwic.herokuapp.com/container";
        fetch(urlForBlockCommit,
        {
            method: 'POST',
            headers: {'Content-Type': 'text/plain'},
            body: JSON.stringify(this.state)
        })
        .then((response)=>{
          //DEBUG response.json().then((obj)=>console.log(obj)).catch((err)=>console.log(err));
        })
        .catch((err)=>console.log(err));
        
    }
    render(){
        let blockInstance = this;
        if(this.state.mode === 0){
            return(
                <div id={this.state._id} style={TasksBlockDivStyle} onDrop={this.drop} onDragOver={this.allowDrop}>
                    <div className="container_title">
                        <h1 onDoubleClick={this.switchMode}>{this.state._title}</h1>
                    </div>
                    {this.state.myTasks.map(function(task){
                        return <Task session_id={blockInstance.state.session_id} ref={blockInstance.addTaskRef} ObjIns={task} PrevOwner={blockInstance.state._id} key={task._id} removeTask={blockInstance.props.removeTask}/>
                    })}
                </div>
            );                  
          } 
        else{
            return(
                <div id={this.state._id} style={TasksBlockDivStyle} onDrop={this.drop} onDragOver={this.allowDrop}>
                    <input type="text" id={'input' + this.state._id}  defaultValue={this.state._title} ></input>
                    <button className="save_buttons" onClick={this.saveBlock}>Save</button>
                    {this.state.myTasks.map(function(task){
                        return <Task session_id={blockInstance.state.session_id} ref={blockInstance.addTaskRef} ObjIns={task} PrevOwner={blockInstance.state._id} key={task._id} removeTask={blockInstance.props.removeTask}/>
                    })}  
                </div>
            );
        }
    }
}
class ColorPicker extends React.Component{

  render(){
      return(
          <div>
              <div className="ColorPickerStyle" style={{backgroundColor: 'white'}} onClick = {()=> this.props.setColorId(0)}></div>
              <div className="ColorPickerStyle" style={{backgroundColor: '#b7ffc8'}} onClick = {()=> this.props.setColorId(1)}></div>
              <div className="ColorPickerStyle" style={{backgroundColor: '#ffb3ba'}} onClick = {()=> this.props.setColorId(2)}></div>
              <div className="ColorPickerStyle" style={{backgroundColor: '#ffffba'}} onClick = {()=> this.props.setColorId(3)}></div>
              <div className="ColorPickerStyle" style={{backgroundColor: '#bae1ff'}} onClick = {()=> this.props.setColorId(4)}></div>
          </div>
      );
  }
}
class Task extends React.Component{
    constructor(props){
        super(props);
        /* mode 0 for view mode, 1 for edit mode*/
        this.state = {
          mode: 0,
          _id: this.props.ObjIns._id,
          _title: this.props.ObjIns._title || "Default title",
          _text: this.props.ObjIns._text || "Default value",
          color_id: this.props.ObjIns.color_id || 0,
          owner_id: this.props.PrevOwner,
          session_id: this.props.session_id || 0
        };
        this.drag = this.drag.bind(this);
        this.switchMode = this.switchMode.bind(this);
        this.saveTask = this.saveTask.bind(this);
        this.preventDrag = this.preventDrag.bind(this);
        this.saveToServer = this.saveToServer.bind(this);
        this.deleteTask = this.deleteTask.bind(this);
        this.setColorId = this.setColorId.bind(this);
    }
    setColorId(colorId){
        this.setState({
            color_id : colorId
        });
    }
    drag(ev){
        ev.dataTransfer.setData("taskObj", JSON.stringify(this.state));
    }
    preventDrag(ev){
        ev.preventDefault();
    }
    switchMode(ev){
        /* mode 1 is for modification mode */
        this.setState({
            mode:1
        });
    }
    saveTask(ev){
        /** Executed on button click in task edit mode , mode 0 for view mode*/
        let newTitle = document.getElementById('inputTitle' + this.state._id).value; 
        let newText = document.getElementById('inputText' + this.state._id).value;
        this.setState({
            mode: 0,
            _title: newTitle,
            _text: newText
        }, this.saveToServer);
    }
    deleteTask(){
        /**
            function to delete task by requesting to server and removing from the owner component
        */
        let urlForTaskDelete = "https://bwic.herokuapp.com/task";
        fetch(urlForTaskDelete,
        {
            method: 'DELETE',
            headers: {'Content-Type': 'text/plain'},
            body: JSON.stringify(this.state)
        })
        .then((response)=>{
          //DEBUG
          //response.json().then((obj)=>console.log(obj)).catch((err)=>console.log(err));
        })
        .catch((err)=>console.log(err)); 
        /* Remove task from the owner */
        this.props.removeTask(this.state._id, this.state.owner_id);                             
    }
    saveToServer(){
        /**
            function to send update to server using task id and container id
        */
        let urlForTaskCommit = "https://bwic.herokuapp.com/task";
        fetch(urlForTaskCommit,
        {
            method: 'POST',
            headers: {'Content-Type': 'text/plain'},
            body: JSON.stringify(this.state)
        })
        .then((response)=>{
          //DEBUG response.json().then((obj)=>console.log(obj)).catch((err)=>console.log(err));
        })
        .catch((err)=>console.log(err));
    }
    render(){
        /**
            Markdown convert the text
        */
        let mdConverter = new showdown.Converter();
        let taskText = this.state._text;
        let taksTextHTML =  mdConverter.makeHtml(taskText);
        let htmlObj = {
            __html: taksTextHTML
        };
        let taskViewStyleUpdated;
        let taskEditStyleUpdated;
        switch(this.state.color_id){
            case 0:
                taskViewStyleUpdated = {...TaskViewStyle, backgroundColor:'white'}; 
                taskEditStyleUpdated = {...TaskViewStyle, backgroundColor:'white'}; 
                break;
            case 1:
                taskViewStyleUpdated = {...TaskViewStyle, backgroundColor:'#b7ffc8'}; 
                taskEditStyleUpdated = {...TaskViewStyle, backgroundColor:'#b7ffc8'};
                break;
            case 2:
                taskViewStyleUpdated = {...TaskViewStyle, backgroundColor:'#ffb3ba'}; 
                taskEditStyleUpdated = {...TaskViewStyle, backgroundColor:'#ffb3ba'};
                break;
            case 3:
                taskViewStyleUpdated = {...TaskViewStyle, backgroundColor:'#ffffba'}; 
                taskEditStyleUpdated = {...TaskViewStyle, backgroundColor:'#ffffba'}; 
                break;
            case 4:
                taskViewStyleUpdated = {...TaskViewStyle, backgroundColor:'#bae1ff'}; 
                taskEditStyleUpdated = {...TaskViewStyle, backgroundColor:'#bae1ff'}; 
                break;
            default:
                taskViewStyleUpdated = {...TaskViewStyle, backgroundColor:'white'}; 
                taskEditStyleUpdated = {...TaskViewStyle, backgroundColor:'white'}; 
                break;
        }
        if(this.state.mode === 0){
            return(
                <div id={this.state._id} style={taskViewStyleUpdated} onDoubleClick={this.switchMode} draggable="true" onDragStart={this.drag}>
                    <div><h4 style={TitleStyle}>{this.state._title}</h4></div>
                    <div dangerouslySetInnerHTML={htmlObj}></div>
                </div>
            );
        } else{
            return(
                <div id={this.state._id} style={taskEditStyleUpdated} draggable="false" onDragStart={this.preventDrag}>
                    <div style={TextContainerStyle} draggable="false" onDragStart={this.preventDrag}>
                        {/* preventDrag stops the text area from being draggable */}
                        <i className="fas fa-times-circle" style={DeleteButtonStyle} onClick={this.deleteTask}></i>
                        <input id={'inputTitle' + this.state._id} draggable="false" onDragStart={this.preventDrag}  style={TitleInputStyle} defaultValue={this.state._title}></input>
                        <br/>
                        <br/>
                        <textarea id={'inputText' + this.state._id} draggable="false" onDragStart={this.preventDrag} style={TextInputStyle} defaultValue={this.state._text}></textarea>
                        <br/>
                        <ColorPicker setColorId={this.setColorId}/>
                        <button className="save_buttons" onClick={this.saveTask}>Save</button>
                    </div>
                </div>                     
            );
        }
    }
}

class Board extends React.Component{
    /**
        Main component, handles first request if already saved, then initialize the blocks and tasks, responsible for passing down 'id' or 'key' to child to allow changes on child 
        to be saved
    */
    constructor(props){
        super(props);
        /* states contain the DOM elements */
        this.state = {
            blockList: [],
            taskList: []
        };    
        /* list of references to the instances */
        this.blockRefs = [];
        this.taskRefs = [];
        /*DEBUG manually set the session id for now*/
        this.session_id = this.props.session._id || 1;
        /* methods binding */
        this.addBlock = this.addBlock.bind(this);
        this.addTask = this.addTask.bind(this);
        this.addBlockRef = this.addBlockRef.bind(this);
        this.addTaskRef = this.addTaskRef.bind(this);
        this.removeTask = this.removeTask.bind(this);
        let selfInstance = this;
        //mode 2
        fetch("https://bwic.herokuapp.com/session/" + this.session_id, {
          method: 'GET'
        }).then((response)=>response.json())
        .then((retrievedBlocks)=> retrievedBlocks.forEach((curBlock)=>{
            let curBlockObj = JSON.parse(curBlock);
            this.setState({
              blockList: this.state.blockList.concat(<TasksBlock instanceObj={curBlockObj} removeTask={this.removeTask} ref={selfInstance.addBlockRef} _id={curBlockObj._id} key={curBlockObj._id} />)
            })
        }));                     
    }
    removeTask(task_id, block_id){
        this.blockRefs.forEach((curBlock)=>{
            if(curBlock.state._id === block_id){
                curBlock.setState({
                  myTasks: curBlock.state.myTasks.filter((curTask)=>{
                      return curTask._id !== task_id
                  })
                }, curBlock.saveToServer);
            }
        });
        this.taskRefs.forEach((curTaskRef)=>{
            if(curTaskRef && (curTaskRef.state._id === task_id)){
                this.setState({
                    taskList: this.state.taskList.filter((curTask)=>{
                        return curTask.props._id !== task_id
                    })
                })
            }
        });
    }
    addBlockRef(instance){
        this.blockRefs = this.blockRefs.concat(instance);
    }
    addTaskRef(instance){
        this.taskRefs = this.taskRefs.concat(instance);
    }
    addBlock(){
        let dummyURLForNewBlockObject = "https://bwic.herokuapp.com/container"              
        let blockObj = {
          _id: null,
          session_id: this.session_id || 0
        };
        /**
          to do : when adding new block, make post request first to save the block and get the id
        */
        fetch(dummyURLForNewBlockObject,
        {
            method: 'post',
            headers: {'Content-Type':'text/plain'},
            body: JSON.stringify(blockObj)
        })
        .then((response)=>response.json())
        .then((response)=>{
            blockObj["_id"] = response._id;
            blockObj["_name"] = "Default"
            let selfInstance = this;
            this.setState({
                blockList: this.state.blockList.concat(<TasksBlock session_id={this.session_id} removeTask={this.removeTask} _name={blockObj._name} ref={selfInstance.addBlockRef} _id={(blockObj._id || this.state.blockList.length)} key={(blockObj._id || this.state.blockList.length)} />)
            }); 
        })
        .catch((err)=>console.log(err));                  
    }
    addTask(){
        
        let dummyURLForNewTaskObject = "https://bwic.herokuapp.com/task"
        let taskObj = {
          _id: null,
          session_id: this.session_id || 0
        };
        /**
          to do : when adding new block, make post request first to save the block and get the id
        */
        fetch(dummyURLForNewTaskObject,
        {
            method: 'post',
            headers: {'Content-Type':'text/plain'},
            body: JSON.stringify(taskObj)
        })
        .then((response)=>response.json())
        .then((response)=>{
            taskObj["_id"] = 'task' + response._id;
    
            let selfInstance = this;
            this.setState({
                taskList: this.state.taskList.concat(<Task session_id={this.session_id} ObjIns={taskObj} ref={selfInstance.addTaskRef} _id={(taskObj._id || this.state.taskList.length)} key={(taskObj._id || this.state.taskList.length)} removeTask={this.removeTask} />) 
            });
        })
        .catch((err)=>console.log(err));
    }
    render(){
        return(
            <div>
                <div class="title-bar">
                    <div class="title-div">
                        <h1 class="title">{this.props.session.name}</h1>                
                    </div>
                </div>
                <div class="action-bar">
                    <div class="action-div">
                        <h3 class="actions">Actions : </h3>
                        <button className="main_buttons main_buttons_color_1" onClick={this.addBlock}>Add Block</button>
                        <button className="main_buttons main_buttons_color_2" onClick={this.addTask}>Add Task</button>
                        <button className="main_buttons main_buttons_color_3" onClick={this.props.viewMain}>Back</button>
                    </div>
                </div>
                <h1 style={SessionHeadingStyle}> {this.props.session.name}</h1>}
                <div>
                    {this.state.taskList.map(function(curTask, index){
                      return(curTask);
                    })}                                                      
                </div>
                <div>
                    {this.state.blockList.map(function(curBlock, index){
                      return(curBlock);
                    })}
                </div>
            </div>
        );
    }
}

export default Board;
