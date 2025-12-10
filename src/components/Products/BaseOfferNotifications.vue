 <template>
    <div class="offerBar">								
        <div class="offerBar--text">
            <span class="offerBar--icon">
                <svg-icon
                    icon-id="discount"
                    icon-viewbox="0 0 24 24"
                ></svg-icon>
            </span>
            Special Limited Offer Get   
            <b> 30 </b>% off Now.
            <a href="#" class="see-more">
            get the offer
            </a>
        </div>				
        <div class="offerBar--countdown">
            Ends in 10:53:43
        </div>		
    </div>
</template>

<script>
export default {

}
</script>

<style lang='scss' scoped>
.offerBar {
	background: linear-gradient(345.63deg, #EBAEA4 -196.47%, #F7C0B7 90.84%);
	padding: rem(20px) rem(48px);
	border-radius: 34px;
	margin-bottom: rem(34px);
	display: flex;
	align-items: center;
	justify-content: space-between;
	height: 64px;
	position: relative;
	z-index: 2;
	overflow: hidden;
	&::before {
		position: absolute;
		content: '';
		width: 100%;
		height: 100%;
		background-image: url('../../assets/images/offer-background.png');
		background-repeat: no-repeat;
		background-size: cover;
		top: 0;
		left: 0;
		z-index: 1;
	}
	&--text {
		font-size: rem(16px);
		font-weight: 400;
		color: var(--textPrimary);
		display:flex;
		align-items: center;
		position: relative;
		z-index: 2;
	}
	b {
		display: inline-block;
		font-weight: 500;
		margin-left: rem(3px);
	}
	&--icon {
		margin-right: rem(13px);
		svg {
		width: 26px;
		color: var(--secondary);
		}
	}
	.see-more {
		font-size: rem(16px);
		font-weight: 700;
		margin-left: rem(12px);
		text-decoration: underline;
		text-transform: uppercase;
	}
	&--countdown {
		font-size: rem(16px);
		font-weight: 500;
		color: var(--textPrimary);
		z-index: 2;
	}
}
</style>