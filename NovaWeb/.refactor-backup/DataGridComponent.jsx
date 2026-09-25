import { Component } from "react";
import axios from 'axios';
import Form from 'react-bootstrap/Form';
import configData from  "../../config.json";
import './DataGridComponent.css'; 

export default class App extends Component{

  constructor(props){
    super(props);

    this.state= {
      title: "Piano di Spedizone",
      buttonCaption: "Carica Dati",
      headersColumns:[],
      items: [],
      comboItems:[],
      id:configData.MENU,
      language : "Italian"
    }
  }

  loadCombo()
  {
    axios.get(`${configData.SERVER_URL}combo?config=${this.state.id}&language=${this.state.language}`,   
      {auth: {
        username: configData.USER_NAME,
        password: configData.PASSWORD
      }
    }).then(res => {
        const comboItems = res.data.values;
        this.setState({ comboItems });
      })
      .catch(err => {
        console.error('Error fetching data:', err);
      });
  }

  loadGrid(filter)
  {
    axios.get(`${configData.SERVER_URL}view?config=${this.state.id}&language=${this.state.language}&filter=${filter}`,   
      {auth: {
        username: configData.USER_NAME,
        password: configData.PASSWORD
      }
    }).then(res => {
        const items = JSON.parse(res.data)
        this.setState({ items });
        if ( items.length > 0){
          var keyNames = Object.keys(items[0]);

          const headers = [];
          var columns = {};
          for (var i = 0; i< keyNames.length;i++)
          {
            columns[keyNames[i]] = keyNames[i];
          }
          headers.push(columns);

          var headersColumns = [];
          headersColumns = Array.from(new Set(headers.flatMap(item => Object.keys(item))));
          this.setState({headersColumns});
        }
      })
      .catch(err => {
        console.error('Error fetching data:', err);
      });
  }

  componentDidMount()
  {
    this.loadCombo();
  }

  showCombo= () =>this.state.comboItems.map((c, i) => {
            return (              
                  <option value={c}>{c}</option> 
              );
          });



  showHeader = () =>this.state.headersColumns.map((k) => {
            return (
                <th>{k}</th>    
              );
          });

  showData = () => this.state.items.map((item) => {
            return (
                <tr>
                    {
                    this.state.headersColumns.map((k) => {
                      return (
                          <td>{item[k]}</td>    
                            );
                        })                      
                    }
                </tr>    
              );
          });

  handleChange=(e)=>{    
    this.loadGrid(e.target.value);
  }
      
  render = () =>
        <div>
          <h4 className="bg-primary text-white text-center p-2">
            { this.state.title }
          </h4>
          <div className="combo">
      <Form.Group controlId="exampleForm.SelectCustom">
      <Form.Label>Seleziona:</Form.Label>
      <Form.Select onChange={this.handleChange} className="select">
            <option></option>
            {this.showCombo()}
          </Form.Select>
          </Form.Group>
</div>
        <table className="table table-striped table-bordered">
          <thead>
            <tr>
                { this.showHeader() }
            </tr>
          </thead>
          <tbody>
            { this.showData() }
          </tbody>
        </table>
    </div>
}
