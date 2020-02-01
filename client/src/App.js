import React from 'react';
import { Chart } from 'react-google-charts';
import Happy from './positive.png';
import Sad from './meh.png';
import Angry from './neg.png';
import Brain from './brain.png';


import './App.css';

class App extends React.Component {
  state = {
    unit: 'week',
  }


  render() {
    return (
      <div className="App">
        <div className="braini">
          <image className="bigbrn" src={Brain}/>
        </div>
        <div class="jumbotron jumbotron-fluid">
          <h1 class="display-4">Let's take a look<br />&emsp;&emsp;at your {this.state.unit}.</h1>
        </div>
        <div className="container">
          <h4 className="summary">Looks like someone's {this.state.unit} was awesome!</h4>
          {//subject to change
          }
          <br />
          <h4 className="moodsum">Let's look at your mood for the {this.state.unit}</h4>
          <div className="mood-chart">
            <Chart
              chartType="LineChart"
              data={[["Day of the Week", "Happiness Levels"], [new Date(2020, 1, 1), 5], [new Date(2020, 1, 2), -3], [new Date(2020, 1, 3), -7], [new Date(2020, 1, 4), 5], [new Date(2020, 1, 5), -1], [new Date(2020, 1, 6), 0], [new Date(2020, 1, 7), 5]]}
              width="100%"
              height="72vh"
              options={{
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
          <h4 className="emo-head">Here's what we think causes your moods</h4>
          <div className="emo-container">
            <div className="happydiv"> 
              <img className="posimg" src={Happy}/>
            </div>
            <div className="pos-box">
              <ul>
                <li> applebee</li>
                <li> ice-cream</li>
                <li> ice-cream</li>
                <li> ice-cream</li>
              </ul>
            </div>
            <div className="mehdiv"> 
              <img className="mehimg" src={Sad}/> 
            </div>
            <div className="meh-box">
              <ul>
                <li> driving</li>
                <li> driving</li>
                <li> driving</li>
                <li> driving</li>
              </ul>
            </div>
            <div className="negdiv"> 
              <img className="negimg" src={Angry}/>
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
                colorAxis: { colors: ['yellow', 'red'] },
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
