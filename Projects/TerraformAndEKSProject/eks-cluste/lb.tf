resource "aws_lb" "my_nlb" {
  name               = "my-nlb"
  internal           = false # Set to true for internal NLB
  load_balancer_type = "network"
  subnets            = aws_subnet.public_subnet[*].id # Use your public subnets
}

resource "aws_lb_target_group" "my_target_group" {
  name     = "my-target-group"
  port     = 80
  protocol = "TCP"
  vpc_id   = aws_vpc.my_vpc.id
}

resource "aws_lb_listener" "my_listener" {
  load_balancer_arn = aws_lb.my_nlb.arn
  port              = 80
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.my_target_group.arn
  }
}

output "nlb_dns_name" {
  value = aws_lb.my_nlb.dns_name
}

