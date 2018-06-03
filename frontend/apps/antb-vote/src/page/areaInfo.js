import React, { Component } from 'react';
import { 
	List,
	Button,
	InputItem,
	WingBlank,
	ImagePicker,
	WhiteSpace
 } from 'antd-mobile';
import TopNavBar from './components/topNavBar';




class AreaInfo extends Component {
  constructor(props) {  
    super(props);  
    this.state = { 
	  name:'东晟府',
	  unitNumber:'3单元402房',
	  certificateNumber:'',
	  certificatePhotos:[],
	}
  }
  savePersonalInfo = () => {
	  
  }
  imagePickerChange = (files,type,index) =>{
	  //console.log(files);
	  this.setState({
		  certificatePhotos:files
	  })
  }
  render() {
    return (
	  <div>
		<TopNavBar title='小区信息'/>
		<div className='peronalInfoForm' >
		  <List>
		    <InputItem
		  	  placeholder = '请输入'
		      value={this.state.name}
		      onChange={name => this.setState({ name })}
		    >小区名称</InputItem>
		    <InputItem
		  	  placeholder = '请输入'
		      value={this.state.unitNumber}
		      onChange={unitNumber => this.setState({ unitNumber })}
		    >单元户号</InputItem>
		    <InputItem
		  	  placeholder = '请输入'
		      value={this.state.certificateNumber}
		      onChange={certificateNumber => this.setState({ certificateNumber })}
		    >产权证号</InputItem>
		    <List>
			  <List.Item >产权证书</List.Item>
		      <ImagePicker 
		        files={this.state.certificatePhotos}
		        onChange={this.imagePickerChange}
		        multiple={true}
			    style={{paddingBottom:5}}
		      />
		    </List>
		  </List>
		</div>
	    <div className='operationBtns'>
		  <WingBlank>
		    <WhiteSpace size="md" />
		    <Button style={style.btn} activeStyle={{backgroundColor:"gray"}}>实名认证</Button>
		    <WhiteSpace size="md" />
		    <Button onClick={this.savePersonalInfo}>保存</Button>
		    <WhiteSpace size="md" />
		  </WingBlank>
	    </div>
      </div>
    );
  }
}
const style = {
	headImgBox:{
	  lineHeight:"80px",
	  fontSize:17,
	  position:'relative',
	  paddingLeft:15
	},
	headImg:{
	  position:'absolute',
	  display:'block',
	  top:10,
	  right:10
	},
	btn:{
	  backgroundColor:"#0cbc0a",
	  color:"#fff",
	},
}; 
export default AreaInfo;
