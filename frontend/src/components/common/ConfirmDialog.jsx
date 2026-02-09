import { Modal } from './Modal'
import { Button } from './Button'

/**
 * ConfirmDialog Component
 */
export const ConfirmDialog = ({ 
  isOpen, 
  onClose, 
  onConfirm, 
  title = '확인',
  message,
  confirmText = '확인',
  cancelText = '취소',
  variant = 'primary'
}) => {
  const handleConfirm = () => {
    onConfirm()
    onClose()
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={title}>
      <div className="mb-6">
        <p className="text-gray-700">{message}</p>
      </div>
      <div className="flex justify-end space-x-3">
        <Button variant="secondary" onClick={onClose}>
          {cancelText}
        </Button>
        <Button variant={variant} onClick={handleConfirm}>
          {confirmText}
        </Button>
      </div>
    </Modal>
  )
}
