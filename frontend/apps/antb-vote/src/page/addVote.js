import React, { Component } from 'react';
import { 
	DatePicker,
	List,
	Button,
	TextareaItem,
	InputItem,
	ImagePicker,
	Picker,
	Switch,
	WingBlank,
	WhiteSpace
 } from 'antd-mobile';
import InputOptionList from './components/inputOptionList';
import TopNavBar from './components/topNavBar';


const nowTimeStamp = Date.now();
const now = new Date(nowTimeStamp);
const electoralRules = [
	{value:'不限',label:'不限',children:[]},
	{value:'规则一',label:'规则一',children:[]},
	{value:'规则二',label:'规则二',children:[]},
]
let eventPhotos = [{
  url: 'https://zos.alipayobjects.com/rmsportal/PZUUCKTRIHWiZSY.jpeg',
  id: '2121',
}, {
  url: 'https://zos.alipayobjects.com/rmsportal/hqQWgTXdrlmVVYi.jpeg',
  id: '2122',
}];
const loadingBtnStyle={
	backgroundColor:'#a17e7e',
	color:'white'
}

class AddVote extends Component {
  constructor(props) {  
    super(props);  
    this.state = { 
	  title:'',
	  describe:'',
	  eventPhotos:eventPhotos,
	  startDate:now,
	  endDate:now ,
	  isMulti:false,
	  isOrot:true,
	  maximum:[2],
	  isAnonymous:false,
	  electoralRule:['不限'],
	  shortListStr:',,',
	  saveLoading:false,
	  addLoading:false,
	  param:props.location.state?props.location.state:[],
	  clicked:'none'
	}
  }

  getShortListStr = (shortListStr) => {
	this.setState({shortListStr:shortListStr})
　}
  imagePickerChange = (files,type,index) =>{
	  //console.log(files);
	  this.setState({
		  eventPhotos:files
	  })
  }
  saveVoteBtnClick = () => {
	this.setState({
	  saveLoading:true,
	})
	let data = {
	  title:this.state.title,
	  describe:this.state.describe,
	  eventPhotos:this.state.eventPhotos,
	  shortListStr:this.state.shortListStr,
	  isMulti:this.state.isMulti,
	  isOrot:this.state.isOrot,
	  maximum:this.state.maximum,
	  isAnonymous:this.state.isAnonymous,
	  startDate:Date.parse(this.state.startDate),
	  endDate:Date.parse(this.state.endDate),
	  electoralRule:this.state.electoralRule,
	};
	console.log(data);
	//window.location.href = '/saveSuccess/6';
  }
  addVoteBtnClick = () => {
	this.setState({
		addLoading:true,
	})
	let data = {
	  title:this.state.title,
	  describe:this.state.describe,
	  eventPhotos:this.state.eventPhotos,
	  shortListStr:this.state.shortListStr.split(',').filter((item) => item.replace(/\s+/g,'')),
	  isMulti:this.state.isMulti,
	  isOrot:this.state.isOrot,
	  maximum:this.state.isMulti?this.state.maximum[0]:1,
	  isAnonymous:this.state.isAnonymous,
	  startDate:Date.parse(this.state.startDate),
	  endDate:Date.parse(this.state.endDate),
	  electoralRule:this.state.electoralRule[0],
	};
	console.log(data);
	//window.location.href = '/addSuccess/6';
  }
  renderMaximumPicker = () => {
	let data = [{value:2,label:2}];
	let count = this.state.shortListStr.split(',').length;
	let countT = this.state.shortListStr.split(',').filter((item) => item.replace(/\s+/g,'')).length;
	let disabled = false;
	if(countT < 3) disabled = true;
	if(this.state.isMulti && count > 2){
	  for(let i = 3;i <= countT;i++){
	  	data.push({value:i,label:i})
	  }
	  return <Picker 
		  disabled={disabled}
	  	  data={data} 
	  	  cols={1} 
	  	  value={this.state.maximum}
	  	  onChange={maximum => this.setState({ maximum })}
	  	  onOk={maximum => this.setState({ maximum })}
	    >
	  	  <List.Item arrow='horizontal'>最多可选</List.Item>
	    </Picker>;
	}
  }
  render() {
    return (
	  <div>
		<TopNavBar title='创建投票'/>
		<List className='addVoteForm'>
		  <InputItem
		    clear
			placeholder = '请输入'
		    value={this.state.title}
		    onChange={title => this.setState({ title })}
		  >投票标题</InputItem>
		  <TextareaItem
		    title='补充描述'
			placeholder = '请输入'
			rows='8'
			autoHeight
		    value={this.state.describe}
		    onChange={describe => this.setState({ describe })}
		  />
		  <List.Item>活动图片</List.Item>
		  <ImagePicker 
			files={this.state.eventPhotos}
			onChange={this.imagePickerChange}
			multiple={true}
		  />
		  
		  <InputOptionList 
		    id='shortList_test' 
			optionListStr={this.state.shortListStr} 
			toParent={this.getShortListStr.bind(this)} 
		  />
		  
		  <List.Item
		    extra={<Switch 
			  checked={this.state.isMulti}
			  onClick={(isMulti) => this.setState({ isMulti })}
			/>}
		  >是否多选</List.Item>
		  {this.renderMaximumPicker()}
		  <List.Item
		    extra={<Switch 
			  checked={this.state.isAnonymous}
			  onClick={(isAnonymous) => this.setState({ isAnonymous })}
			/>}
		  >是否匿名</List.Item>
		  <DatePicker
		    value={this.state.startDate}
		    onChange={startDate => this.setState({ startDate })}
		  >
		    <List.Item arrow='horizontal'>开始日期</List.Item>
		  </DatePicker>
		  <DatePicker
		    value={this.state.endDate}
		    onChange={endDate => this.setState({ endDate })}
		  >
		    <List.Item arrow='horizontal'>结束日期</List.Item>
		  </DatePicker>
		  <Picker 
		    data={electoralRules} 
			cols={1} 
			value={this.state.electoralRule}
		    onChange={electoralRule => this.setState({ electoralRule })}
		    onOk={electoralRule => this.setState({ electoralRule })}
		  >
            <List.Item arrow='horizontal'>选举规则</List.Item>
          </Picker>
		  <List.Item
		    extra={<Switch 
			  checked={this.state.isOrot}
			  onClick={(isOrot) => this.setState({ isOrot })}
			/>}
		  >一房一票</List.Item>
		</List>
		
	    <div className='operationBtns'>
		  <WingBlank>
		    <WhiteSpace size='md' />
		    <Button 
			  loading={this.state.addLoading} 
			  style={this.state.addLoading?loadingBtnStyle:{}} 
			  onClick={this.addVoteBtnClick}
			>
			  {this.state.addLoading?'创建中 Loading':'创建投票'}
			</Button>
		    <WhiteSpace size='md' />
		    <Button 
			  loading={this.state.saveLoading} 
			  style={this.state.saveLoading?loadingBtnStyle:{}} 
			  onClick={this.saveVoteBtnClick}
			>
			  {this.state.saveLoading?'保存中 Loading':'暂时保存'}
			</Button>
		    <WhiteSpace size='md' />
		  </WingBlank>
	    </div>
      </div>
    );
  }
}

export default AddVote;
