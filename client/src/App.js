import React from 'react';
import { Chart } from 'react-google-charts';
import Happy from './udhappy.png';
import Angry from './udsad.png';

import Modal from 'react-awesome-modal';
import './App.css';

class App extends React.Component {
  state = {
    unit: 'week',
    timeline: [],
    popupVisible: true,
  }

  closeModal() {
    this.setState({
      popupVisible: false
    });
  }
  componentDidMount() {
    console.log("Requesting timeline data")
    fetch('http://192.168.12.1:5000/notes/timeline')
    .then( res => res.json() )
    .then( (data) => {
      for( let i=0; i <data.length; i++ ) {
        let arr = data[i].timestamp;
        data[i].timestamp = new Date(arr[0],arr[1]-1,arr[2]);
      }
      this.setState({ timeline: data });
      console.log(this.state.timeline);
    })
    .catch(console.log)

    
  }

  render() {
    console.log(this.state.timeline.length)
    let values = [["Day of the Week", "Mental Wellbeing", { role: "tooltip", type: "string", p: { html: true } }]];
    for( let j=15; j < this.state.timeline.length; j++) {
      let point = [
        this.state.timeline[j].timestamp, 
        this.state.timeline[j].score.compound, 
        `<b>${this.state.timeline[j].title}</b><br><i>Mental Wellbeing: </i> ${this.state.timeline[j].score.compound}`];
      if( j < 22) values.push(point);
    }
    return (
      <div className="App">
        <Modal visible={this.state.popupVisible} width="600" effect="fadeInUp" onClickAway={() => this.closeModal()}>
          <div class="popup">
            <h4>Looks like someone had an awesome week!</h4>
            <p>Bruh</p>
            <a href="javascript:void(0);" onClick={() => this.closeModal()}>See your mental health stats</a>
          </div>
        </Modal>
        <div class="jumbotron jumbotron-fluid">
          <h1 class="display-4"> Appname.</h1>
          <p class="lead">something something somethnig</p>
        </div>
        <div className="container">
          {/* <h4 className="summary">Looks like someone's {this.state.unit} was awesome!</h4> */}
          {//subject to change
          }
          <h4 className="moodsum">Let's look at your mood for the {this.state.unit}</h4>
          <div className="mood-chart">
            <Chart
              chartType="LineChart"
              data={values}
              width="100%"
              height="50vh"
              options={{
                tooltip: { isHtml: true, trigger: "visible" },
                explorer: { axis: 'horizontal', keepInBounds: true },
                hAxis: {
                  title: '',

                },
                vAxis: {
                  title: '',
                  textPosition: 'none',
                },
                series: {
                  0: { curveType: 'function' },
                },
              }}
            />
          </div>

          <br />
          <h4 className="emo-head">This is what makes you happy.</h4>
          <div className="emo-container">
            <div className="happydiv">
              <img className="posimg" src={Happy} />
            </div>
            <div className="pos-box">
              <ul>
                <li> applebee</li>
                <li> ice-cream</li>
                <li> ice-cream</li>
                <li> ice-cream</li>
              </ul>
            </div>
            {/* <div className="mehdiv"> 
              <img className="mehimg" src={Sad}/> 
            </div>
            <div className="meh-box">
              <ul>
                <li> driving</li>
                <li> driving</li>
                <li> driving</li>
                <li> driving</li>
              </ul>
            </div> */}
            <h4 className="emo-head1">This is what makes you Sad.</h4>
            <div className="negdiv">
              <img className="negimg" src={Angry} />
            </div>
            <div className="neg-box">
              <ul>
                <li> shawn</li>
                <li> shawn</li>
                <li> shawn</li>
                <li> ice-cream</li>
              </ul>
            </div>
          </div>
          <br />
          <h4 className="emo-head">We noticed that you care about these a lot</h4>
          <div className="bubble">
            <Chart
              width={'500px'}
              height={'300px'}
              chartType="BubbleChart"
              loader={<div>Loading Chart</div>}
              data={[
                ['ID', 'X', 'Y', 'Temperature'],
                ['', 80, 167, 120],
                ['', 79, 136, 130],
                ['', 78, 184, 50],
                ['', 72, 278, 230],
                ['', 81, 200, 210],
                ['', 72, 170, 100],
                ['', 68, 477, 80],
              ]}
              options={{
                colorAxis: { colors: ['#00fff0', 'red'] },
                vAxis: {
                  gridlines: {
                    color: 'transparent',
                    textPosition: 'none',
                  }
                },
                hAxis: {
                  gridlines: {
                    color: 'transparent',
                    textPosition: 'none',
                  }
                }
              }}
              rootProps={{ 'data-testid': '2' }}
            />
          </div>
          <p>Introspect on these desires. In our experience, we notice that happiness levels are strongly related to your desires.</p>
          <p>People with fewer desires tend to be happier - eliminate desires by meeting them or deciding on what's truly important.</p>
          <h4>Congratulations! Here's what you did this week</h4>
          <div className="temp">
            { //FOR SHAWN FIRST
              //THEN FOR KUNAL
              //Insert list of accomplishments
            }
          </div>
        </div>
      </div>


    );
  }

}

export default App;