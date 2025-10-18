import { Component } from "react";
import './MenuComponent.css'; 

export default class MenuComponents extends Component{

    constructor(props){
        super(props);
        this.state = { menu: 0}
    }

render = () =>
    <div>
        <div className="topnav">
            <a className="active" href="/">Home</a>
        </div>
    </div>
}

    
