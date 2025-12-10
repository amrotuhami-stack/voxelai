<template>
    <div>
        <!-- <a href="#" v-b-modal="'profile-modal'">Add New Patient</a> -->
        <!-- The modal -->
        <b-modal id="profile-modal" centered>
            <div class="modal-title">
                Complete your profile
            </div>
            <p>Let's start with your first service!</p>
            <form>
                <div class="form-group">
                    <input type="number" class="form-control" required="" name="name" placeholder="Phone number"
                    />
                    <label class="control-label">Phone number</label>
                </div>
                <div class="form-group">
                    <input type="text" class="form-control" required="" name="name" placeholder="Speciality"
                    />
                    <label class="control-label">Speciality</label>
                </div>
                <div class="form-group">
                    <input type="text" class="form-control" required="" name="name" placeholder="Nickname (Optional)"
                    />
                    <label class="control-label">Nickname (Optional)</label>
                </div>
                <div class="inline-buttons">
                    <button type="button" class="btn btn-primary">Save</button>
                    <a href="javascript:void(0)" class="link" @click="hideModal">Maybe Later</a>
                </div>
            </form>
        </b-modal>
    </div>
</template>

<script>
export default {
	// props: {
	// 	service: Array,
	// },
	// data() {
	// 	return {
	// 		value: 40,
	// 		max: 100,
	// 	};
	// },
	methods: {
      
      hideModal() {
        this.$refs['profile-modal'].hide()
      }
    },
	data() {
		return {
			value: '',
			selected: null,
			options: [
				// { value: null, text: 'Please select an option' },
				{ value: null, text: 'Gender' },
				{ value: 'a', text: 'Select patient' },
				{ value: 'b', text: 'Selected Option' },
				{
					value: { C: '3PO' },
					text: 'This is an option with object value',
				},
				{ value: 'd', text: 'This one is disabled', disabled: true },
			],
		};
	},
};
</script>

<style lang="scss" scoped>

</style>
