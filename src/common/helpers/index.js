export const formatIds = (_id) => {
    if(_id < 10)
        return '000'+ _id
    else if (_id > 9 && _id < 100)
        return '00' + _id
    else if (_id > 99 && _id < 1000)
        return '0' + _id
    else
        return _id
}


export const serviceIsCompleted = (service) => {
	if(service.phases.length == 0)
		return false

    let requiredFiles = []
	let teeth_chart = null


	// [Important] for service from Photon Lab
	if(!service.service_data) return true;

	// Get Required Files for service and check if teeth chart are required
	if('caseType' in service.service_data && service.service_data.caseType != null) {
		if(service.service_data.caseType.children.length > 0) {
			if('patientType' in service.service_data && service.service_data.patientType != null) {
				requiredFiles = service.service_data.patientType.required_files
				teeth_chart = service.service_data.patientType.teeth_chart
			}
			else {
				return false
			}
		}
		else {
			requiredFiles = service.service_data.caseType.required_files
			teeth_chart = service.service_data.caseType.teeth_chart
		}
	}
    else {
    	return false
    }
	
	// Check if all required files are uploaded
	let allFilesUploaded = true
	requiredFiles.forEach((file) => {
		if(file.is_required) {
			let fileExist = service.service_data.files.findIndex((item) => item.name === file.name)
			let fileUploaded = service.files.findIndex((item) => item.name === file.name)
			if(fileExist == -1 || fileUploaded == -1) {
				allFilesUploaded = false
			}
		}
	})
	if(!allFilesUploaded) {
		return false
	}
	// Check if implanet chart are uploaded
	if(teeth_chart) {
		if(!('implant' in service.service_data) || service.service_data.implant == null) {
			return false
		}
	}
	if(('patient' in service.service_data) && ('product' in service.service_data) && ('files' in service.service_data)) {
		return true
	}
}


export const clientDoctorFilesStatus = (service) => {
	/// [Important] This for service come from Photon
	if (!service.service_data) return 'approved-photon';

	if('files_status' in service.service_data) {
		return service.service_data.files_status
	}
	else {
		return 'approved'
	}
}

export const serviceStatusMessege = (service) => {
	// For AI Analysis Services
	if(service.order_line_obj.product_obj.product_class == 'online-ai-service') {
		let caseRemaining = service.order_line_obj.product_obj.subscription_size - service.order_line_obj.used_cases
		if(caseRemaining > 0) {
			return  {
				clientClass: 'completed',
				clientMessege: `Available - ${caseRemaining} Cases Remaining`,
			}
		}
		else {
			return  {
				clientClass: 'failed',
				clientMessege: `Expired - 0 Cases Remaining`,
			}
		}
	}

	// For Digital Services
	let status = {class: '', messege: ''}
	let currentPhase = -1

	if(!serviceIsCompleted(service)) {
		status = {
			class: 'notStarted',
			messege: 'Waiting doctor to submit files',
			clientClass: '',
			clientMessege: 'Complete your service to get results',
		}
	}
	else {
		if(clientDoctorFilesStatus(service) == 'waiting') {
			status = {
				class: 'delayed',
				messege: 'Doctor waiting approvel on service files',
				clientClass: 'pending',
				clientMessege: 'Pending - Wait for your files to be approved',
			}
		}
		else if(clientDoctorFilesStatus(service) == 'rejected') {
			status = {
				class: 'inProgress',
				messege: 'Waiting doctor to correct service files',
				clientClass: 'failed',
				clientMessege: 'Rejected - Your service files rejected, change them',
			}
		}
		else if(clientDoctorFilesStatus(service) == 'approved-photon') {
			status = {
				class: 'completed',
				messege: `Completed Service`,
				clientClass: 'completed',
				clientMessege: 'Completed - All service phases approved',
			}
		}
		else {
			if(service.phases.length > 0) {
				let index = 0
				while(currentPhase == -1 && index < service.phases.length) {
					if(service.phases[index].status == 'approved') {
						index = index + 1
					}
					else {
						currentPhase = index
					}
				}
				if(currentPhase == -1) {
					status = {
						class: 'completed',
						messege: `Service Completed`,
						clientClass: 'completed',
						clientMessege: 'Completed - All service phases approved',
					}
				}
				else if(service.phases[currentPhase].status == 'rejected') {
					status = {
						class: 'rejected',
						messege: `Phase (${currentPhase + 1}) rejected by doctor`,
						clientClass: 'failed',
						clientMessege: `Rejected - You have reject phase (${currentPhase + 1}) files`,
					}
				}
				else if(service.phases[currentPhase].status == 'new') {
					status = {
						class: 'delayed',
						messege: `Doctor waiting to start phase (${currentPhase + 1})`,
						clientClass: 'pending',
						clientMessege: `Pending - Wait to start phase (${currentPhase + 1})`,
					}
				}
				else {
					let numberOfEmptyFiles = service.phases[currentPhase].deleiver_fields.filter((item) => item.value == '').length
					if(numberOfEmptyFiles == 0) {
						status = {
							class: 'inProgress',
							messege: `Waiting approvel on phase (${currentPhase + 1})`,
							clientClass: 'cancelled',
							clientMessege: `In Progress -  Phase (${currentPhase + 1}) files have been delivered. Check it`,
						}
					}
					else {
						status = {
							class: 'delayed',
							messege: `Doctor waiting phase (${currentPhase + 1}) files`,
							clientClass: 'cancelled',
							clientMessege: `In Progress - Working on phase (${currentPhase + 1}) files`,
						}
					}
				}
			}
		}
	}
	return {...status, phase: currentPhase}
}

