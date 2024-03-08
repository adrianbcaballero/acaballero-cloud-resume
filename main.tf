provider "aws" {
  region = "us-west-1"
}

//test for plan action
resource "random_pet" "server" {}
