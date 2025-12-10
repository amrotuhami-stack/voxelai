<template>
	<div>
		<!--<div class="inner-title">
			I want my Guide to be supported on:
		</div> !-->
		<div class="CaseList" v-if="product && caseDefinitions.length">
			<div class="card CaseList__item" :class="selectedCaseType && selectedCaseType.id === item.id ? 'active' : ''" v-for='item in caseDefinitions' :key="item.id" @click="updateCaseType(item)">
				<div class="card__body">
					<div>
						<div class="image" v-if="item.image">
							<img :src="item.image" :alt="item.slug" class="img-fluid" width="48px" height="48px"/>
						</div>
						<p>
							{{item.title}}<span v-if="item.Descrption">{{item.Descrption}}</span>
						</p>
						<span v-if="selectedCaseType && selectedCaseType.id === item.id" class="checked"></span>
					</div>
				</div>
			</div>
		</div>
		<div class="patientType" v-if="selectedCaseType && selectedCaseType.children.length">
			<div class="inner-title">
				Select your patient type
				<svg-icon
					icon-id="info-circle"
					icon-viewbox="0 0 24 24"
				></svg-icon>
			</div>
			<div class="row">
				<div class="col-md-4 col-sm-6"  v-for='item in selectedCaseType.children' :key="item.id" @click="updatePatientType(item)">
					<div class="contentBox" :class="selectedPatientType && selectedPatientType.id == item.id ? 'active' : ''">
						<div class="image">
							<img :src="item.image" :alt="item.slug" />
						</div>
						<h4>
							{{item.title}}
						</h4>
						<ul>
							<li v-for="(text , index) in formatDescription(item.Descrption)" :key="text + index">
								{{text}}
							</li>
						</ul>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

export default {
	props: {
		product: Object,
		updateService: Function,
		service: Object,
		readOnly: {
      		type: Boolean,
      		default: false,
    	},
	},
	data(){
		return{
			selectedCaseType: null,
			selectedPatientType: null,
			caseDefinitions: [],
		}
	},
	created() {
		this.caseDefinitions = this.product.case_definitions[0].case_definition.children
		if(this.service && this.service.service_data) {
			this.selectedCaseType = this.service.service_data.caseType
			this.selectedPatientType = this.service.service_data.patientType
		}
	},
	watch:  {
		service() {
			if(this.service && this.service.service_data) {
				this.selectedCaseType = this.service.service_data.caseType
				this.selectedPatientType = this.service.service_data.patientType
			}
		}
	},
	methods: {
		updateCaseType(_item){
			if(!this.readOnly) {
				this.selectedCaseType = _item;
				this.updateService({caseType: _item, patientType: null})
			}
		},
		updatePatientType(_item){
			if(!this.readOnly) {
				this.selectedPatientType = _item;
				this.updateService({patientType: _item})
			}
		},
		formatDescription(_dis) {
			if(_dis) {
				return _dis.split('<br>')
			}
		}
	}
};
</script>

<style lang="scss" scoped>
.CaseList {
	margin-bottom: rem(15px);
	.card{
		border: 1px solid #e9e9e9;
		border-radius: 12px;
		cursor: pointer;
		&__body{
			@media screen and (max-width: 991px) {
				padding-right: 35px;
			}
			> div {
				display: flex;
				align-items: center;
				p {
					margin-bottom: 0;
					margin-top: 0;
					margin-left: rem(20px);
					font-weight: 500;
					font-size: rem(16px)!important;
					color: var(--textPrimary)!important;
					text-transform: capitalize;
					span {
						margin-bottom: 0;
						font-weight: 400;
						color: var(--default);
						display: block;
					}
				}
				.image {
					background-color: #f5f5f5;
					border-radius: rem(8px);
					padding: rem(5px);
				}
			}
			.checked {
				background-image: url("data:image/svg+xml,%3Csvg width='20' height='14' viewBox='0 0 20 14' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M17.0565 0.722556C17.5772 0.201857 18.4215 0.201857 18.9422 0.722556C19.4228 1.2032 19.4598 1.95951 19.0531 2.48256L18.9422 2.60817L8.27549 13.2748C7.79485 13.7555 7.03854 13.7925 6.51548 13.3858L6.38987 13.2748L1.05654 7.94151C0.535841 7.42081 0.535841 6.57659 1.05654 6.05589C1.53719 5.57524 2.29349 5.53827 2.81655 5.94497L2.94216 6.05589L7.33268 10.4454L17.0565 0.722556Z' fill='%231A90D2'/%3E%3C/svg%3E%0A");
				background-repeat: no-repeat;
				width: 20px;
				height: 14px;
				position: absolute;
				right: rem(33px);
				top: 50%;
				transform: translateY(-50%);
				content: '';
				@media screen and (max-width: 991px) {
					right: 15px;
				}
			}
		}
	}
	&__item {
		position: relative;
		&:not(:last-child) {
			margin-bottom: rem(15px);
		}
		&.active {
			&.card {
				border-color: var(--primary);
				.image {
					background-color: #eef7fb;
				}
			}
			.checked {
				display: inline-block;
			}

		}
	}
}
.patientType {
	margin-top: rem(25px);
	.contentBox {
		padding: rem(16px);
		height: 100%;
		@media screen and (max-width: 991px) {
			margin-bottom: 15px;
			height: calc(100% - 15px);
		}
		.image {
			text-align: center;
			background: #F5F5F5;
			border-radius: 6px;
			max-height: 125px;
			display: flex;
			align-items: center;
			justify-content: center;
			img {
				max-height: 125px;
			}
		}
		h4 {
			margin-top: rem(20px);
			margin-bottom: rem(12px);
			font-size: rem(16px);
			text-transform: capitalize;
		}
		ul {
			margin-left: rem(20px);
			list-style: disc;
			li {
				font-size: rem(14px);
				font-weight: 400;
				color: var(--default);
				line-height: 1.1;
				margin-bottom: rem(0px);
				&:not(:last-child) {
					margin-bottom: rem(12px);
				}
				&::marker {
					color: #a8d5ee;
					font-size: rem(20px);
				}
			}
		}
		&.active {
			border-color: var(--primary);
			.image {
				background: #EEF7FB;
			}
		}
	}
}
</style>
