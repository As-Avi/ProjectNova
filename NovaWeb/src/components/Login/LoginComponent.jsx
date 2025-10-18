import { Component } from "react";
import App from '../DataGrid/DataGridComponent'
import axios from 'axios';
import configData from  "../../config.json";
import './LoginComponent.css'; 
import { Alert } from "react-bootstrap";
import Form from 'react-bootstrap/Form';
import g from "../../global.jsx"
export default class LoginComponents extends Component{

  values = configData.PROCEDURE;

  constructor(props){
    super(props);

    

    this.state= {
      buttonCaption: "Esegui",
      showData:false,
      show:false,
      procedure:[],
      errorMessage:'',
      user: window.user,
      password: window.pwd
    }

    configData.MENU = "";
    

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleUserChange = this.handleUserChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
  }

  
  login(user)
  {    

    axios.get(`${configData.SERVER_URL}auth`,   
      {auth: {
        username: this.state.user,
        password: this.state.password
      }
    }).then(res => {
        if (res.data === "OK"){        
          this.setState({ showData: true });          
        }
      })
      .catch(err => {
        console.error('Error fetching data:', err);
        this.setState({ show: true });
        this.setState({errorMessage : err.response.data.detail});
      });
  }

  navigate = () => {
    return (
    <div lassName="input-group">
      <input  type = "submit" className="btn btn-success m-1" value= { this.state.buttonCaption }/>

            {this.state.show && (
                <Alert
                    variant="danger"
                    onClose={() => console.log('')}
                    >
                    
                    <Alert.Heading>Error</Alert.Heading>
                    <p>{this.state.errorMessage}</p>
                </Alert>
            )}

    </div>
  );
  }

  handleUserChange(event) {
    this.setState({user: event.target.value});
  }

  handlePasswordChange(event) {
    this.setState({password: event.target.value});
  }
  

  handleSubmit(event) {

    if ( configData.MENU === "")
    {
        this.setState({ show: true });
        this.setState({errorMessage : "Scegliere una procedura."});           
    }
    else{
      this.login(this.state.user);      
    }
    event.preventDefault();
  }

  handleChange=(e)=>{    
    configData.MENU = e.target.value;
  }

createLoginForm = () => {
  return (
    <div  className="Auth-form-container">
      <form className="Auth-form" onSubmit={this.handleSubmit}>
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Inserisci le Credenziali</h3>
          <div className="input-group">
            {/* <span className="input-group-text">
              <i><FontAwesomeIcon icon={faUser} /></i>
            </span> */}
            <input
              className="form-control mt-1"
              placeholder="Utente"
              value={this.state.user} onChange={this.handleUserChange}
            />
          </div>
          <div className="input-group">
            {/* <span className="input-group-text">
              <i><FontAwesomeIcon icon={faLock} /></i>
            </span> */}
            <input
              className="form-control mt-1"
              placeholder="Password"
              type="password"
              value={this.state.password} onChange={this.handlePasswordChange}
            />
          </div>
        <div className="menuScelta">
          <Form.Label>Seleziona:</Form.Label>
        <Form.Select onChange={this.handleChange}>
                {this.values.map((val) => (
                  <option key={val} value={val}>{val}</option>
                ))}
          </Form.Select>
        </div>
          {this.navigate()}

        </div>
      </form>
    </div>
  );
}

//Decide quale componente mostrare
render = () =>
    <div>
      {!this.state.showData && this.createLoginForm()}
      {this.state.showData && <App />}
    </div>
}


