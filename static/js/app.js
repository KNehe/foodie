
const deleteObject = (event, type) => {
    let msg = ''
    
    switch (type) {
    case 'DELETE_ACCOUNT':
        msg = 'Are you sure you want to delete your account ?'
        break;
    case 'DELETE_FOODIE':
        msg = 'Are you sure you want to delete this foodie ?'
        break;
    case 'DELETE_COMMENT':
        msg = 'Are you sure you want to delete this comment ?'
        break;
    default:
        msg = 'Are you sure you want to delete ?'    
    }

    let result = confirm(msg)

    if (!result){
        event.preventDefault()
    }
}
