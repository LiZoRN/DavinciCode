import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom'

import VoteIndex from './page/voteIndex';
import AddVote from './page/addVote';
import AddSuccess from './page/addSuccess';
import SaveSuccess from './page/saveSuccess';
import VoteSquare from './page/voteSquare';
import VotePage from './page/votePage';
import MyVote from './page/myVote';
import AffirmSuccess from './page/affirmSuccess';
import PersonalInfo from './page/personalInfo';
import AreaInfo from './page/areaInfo';

class App extends Component {
  render() {
    return (
		<Switch>
		  <Route exact path='/' component={VoteIndex}/>
		  <Route path='/add' component={AddVote}/>
		  <Route path='/addSuccess/:voteId' component={AddSuccess}/>
		  <Route path='/saveSuccess/:voteId' component={SaveSuccess}/>
		  <Route path='/voteSquare' component={VoteSquare}/>
		  <Route path='/votePage/:voteId' component={VotePage}/>
		  <Route path='/myVote' component={MyVote}/>
		  <Route path='/affirmSuccess' component={AffirmSuccess}/>
		  <Route path='/personalInfo' component={PersonalInfo}/>
		  <Route path='/areaInfo' component={AreaInfo}/>
		</Switch>
    );
  }
}

export default App;
