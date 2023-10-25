variable "ami" {
  description = "Value of the ami for the EC2 instance"
  type    = string
  default = "ami-0efcece6bed30fd98" #ubuntu 22.04 LTS
}

variable "key_name" {
  description = "Name of the SSH keypair to use in AWS."
  default     = "aws-hw-keypair"
}