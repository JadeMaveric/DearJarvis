import React from 'react';

import './App.css';

class App extends React.Component {
  state = {
    unit: 'week',
  }
  render() {
    return (
      <div className="App">
        <div class="jumbotron jumbotron-fluid">
            <h1 class="display-4">Let's take a look<br />&emsp;&emsp;at your {this.state.unit}.</h1>
        </div>
        <div className=" container">
          <h4>Let's look at your mood for the {this.state.unit}</h4>
          <div className="temp">
            { //FOR SHAWN
              //Insert line graph of happiness wrt day here
            }
          </div>
          <br />
          <h4>Here's what we think causes your moods</h4>
          <div className="temp">
            { //FOR KUNAL
              // Make a table with mood images on one side and causes on the other
            }
          </div>
          <br />
          <h4>We noticed that you care about these a lot</h4>
          <div className="temp">
            { //FOR SHAWN
              //Insert bubble graph of desires here
            }
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
