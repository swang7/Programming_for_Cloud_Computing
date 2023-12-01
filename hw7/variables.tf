variable "prefix" {
  description = "The prefix which should be used for all resources in this exercise"
  default = "az-terra"
}

variable "location" {
  description = "The Azure Region in which all resources in this exercise should be created."
  default = "westus3"
}

variable "key_name" {
  description = "Name of the SSH keypair to use in AWS."
  default     = "aws-hw-keypair"
}