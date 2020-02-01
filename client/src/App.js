import React from 'react';
import { Chart } from 'react-google-charts';
import './App.css';

class App extends React.Component {
  state = {
    unit: 'week',
    timeline: [],

  }

  componentDidMount() {
    fetch('http://192.168.12.1:5000/notes/timeline')
    .then( res => res.json() )
    .then( (data) => {
      for( let i=0; i < data.length; i++ ) {
        let arr = data[i].timestamp;
        data[i].timestamp = new Date(arr[0],arr[1],arr[2],arr[3],arr[4],arr[5]);
      }
      this.setState({ timeline: data });
      // console.log(this.state.timeline);
    })
    .catch(console.log)
  }

  render() {
    let values = [["Day of the Week", "Happiness Level"]];
    this.state.timeline.forEach( note => {
      let point = [note.timestamp, note.score.compound]
      values.push(point);
    });
    return (
      <div className="App">
        {//this.timeStampMaker(this.state.timeline[0].timestamp)}
        }<div class="jumbotron jumbotron-fluid">
          <h1 class="display-4">Let's take a look<br />&emsp;&emsp;at your {this.state.unit}.</h1>
        </div>
        <div className="container">
          <h4 className="summary ">Looks like someone's {this.state.unit} was awesome!</h4>
          <br />
          <h4 className="moodsum">Let's look at your mood for the {this.state.unit}</h4>
          <div className="mood-chart">
            <Chart
              chartType="LineChart"
              data={values}
              width="100%"
              height="400px"
              options={{
                explorer: {axis: 'horizontal', keepInBounds: true},
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
          <h4>Here's what we think causes your moods</h4>
          
          <br />
          <h4>We noticed that you care about these a lot</h4>
          <div className="desire-chart">
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
