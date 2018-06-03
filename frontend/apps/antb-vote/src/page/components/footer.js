import React, { Component } from 'react';
import { Link } from 'react-router-dom'





const iconCategory = require('../../icon/Category.svg');
const iconCategoryActive = require('../../icon/Category_active.svg');
const iconAccount = require('../../icon/account.svg');
const iconAccountActive = require('../../icon/account_active.svg');

class Footer extends Component {
  constructor(props){
    super(props)
    this.state = {
		pageIndex:this.props.pageIndex?this.props.pageIndex:0,
	}
  }
  renderVoteSquareButton(){
	  var index = this.state.pageIndex;
	  if(index !== 1){
		return (
			<Link to='/voteSquare'>
			  <div className="footerButton">
				<img alt={iconCategory} src={iconCategory} /><br />
				投票广场
			  </div>
			</Link>);
	  }else{
		return (
			<div className="footerButton footerButton_active">
				<img alt={iconCategoryActive} src={iconCategoryActive} /><br />
				投票广场
			</div>);
	  }
  }
  renderMyVoteButton(){
	  var index = this.state.pageIndex;
	  if(index !== 2){
		return (
			<Link to='/myVote'>
			  <div className="footerButton footerButton_r">
				<img alt={iconAccount} src={iconAccount} /><br />
				我的投票
			  </div>
			</Link>);
	  }else{
		return (
			<div className="footerButton footerButton_r footerButton_active">
				<img alt={iconAccountActive} src={iconAccountActive} /><br />
				我的投票
			</div>);
	  }
  }
  render() {
    return (
	  <div className='footer'>
		<Link to='/add'>
		  <div className='addVoteButton'>
			<span></span>
			<span></span>
		  </div>
		</Link>
		{this.renderVoteSquareButton()}
		{this.renderMyVoteButton()}
		
	  </div>
    );
  }
}

export default Footer;
